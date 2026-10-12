# -*- coding: utf-8 -*-
# DaVinci Resolve Deliver render-end script (Windows and macOS)
# Select this script and set "Trigger script at" to End.

import datetime
import io
import os
import shlex
import subprocess
import sys
import tempfile

SCRIPT_NAME = "DaVinci Resolve 渲染完成自动关机脚本"
AUTHOR = "莫莫先生"
HOMEPAGE = "https://space.bilibili.com/255947051"
RESULT = "渲染作业已结束。"


def _desktop_dir():
    if sys.platform == "win32":
        # Resolve Windows' actual Desktop location, including OneDrive redirection.
        import ctypes
        path = ctypes.create_unicode_buffer(32768)
        result = ctypes.windll.shell32.SHGetFolderPathW(None, 0x10, None, 0, path)
        if result != 0 or not path.value:
            raise OSError("Windows 桌面目录不可用")
        return path.value
    if sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~"), "Desktop")
    raise OSError("当前系统暂不支持")


def _log_result(message):
    try:
        desktop = _desktop_dir()
        if not os.path.isdir(desktop):
            os.makedirs(desktop)
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(desktop, "DaVinci_Render_Result_{}.txt".format(stamp))
        with io.open(path, "w", encoding="utf-8") as f:
            f.write("DaVinci Resolve 渲染结束脚本结果\r\n")
            f.write("完成时间: {}\r\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            f.write("结果: {}\r\n".format(RESULT))
            f.write("\r\n=========================\r\n")
            f.write("{}\r".format(SCRIPT_NAME))
            f.write("作者：{}\r".format(AUTHOR))
            f.write("主页：{}\r".format(HOMEPAGE))
        return path
    except Exception:
        # Keep the failure visible in the Resolve console; never create a log elsewhere.
        print("DaVinci 渲染结果日志写入桌面失败。")
        return None


def _start_windows_countdown():
    # A separate console owns the countdown so it can outlive Resolve.
    command = (
        "Write-Host '========================================' -ForegroundColor DarkGray; "
        "Write-Host '{}' -ForegroundColor Cyan; Write-Host ''; "
        "Write-Host '作者：{}'; Write-Host '主页：{}'; "
        "Write-Host '========================================' -ForegroundColor DarkGray; "
        "Write-Host ''; Write-Host 'DaVinci Resolve 渲染作业已结束。'; "
        "Write-Host '结果：{}'; Write-Host ''; "
        "Write-Host '倒计时期间按任意键可取消自动关机。'; Write-Host ''; "
        "for ($i = 30; $i -ge 1; $i--) {{ "
        "Write-Host -NoNewline (\"`r剩余 {{0,2}} 秒  \" -f $i); "
        "if ([Console]::KeyAvailable) {{ [Console]::ReadKey($true) | Out-Null; "
        "Write-Host ''; Write-Host ''; Write-Host '已取消自动关机。'; "
        "Write-Host ''; Write-Host '按任意键关闭此窗口。'; "
        "$null = [Console]::ReadKey($true); exit }}; "
        "if ($i -eq 10) {{ Write-Host ''; Write-Host '正在请求 DaVinci Resolve 安全退出…'; "
        "$resolve = @(Get-Process -Name 'Resolve','DaVinciResolve' -ErrorAction SilentlyContinue); "
        "if ($resolve.Count -gt 0) {{ $resolve | ForEach-Object {{ $null = $_.CloseMainWindow() }}; "
        "$stillRunning = $false; foreach ($p in $resolve) {{ if (-not $p.WaitForExit(10000)) {{ $stillRunning = $true }} }}; "
        "if ($stillRunning) {{ Write-Host 'DaVinci Resolve 未正常退出，正在强制结束 Resolve 进程…'; "
        "$resolve | Stop-Process -Force -ErrorAction SilentlyContinue }} }} }}; "
        "Start-Sleep -Seconds 1 }}; "
        "Write-Host ''; Write-Host 'DaVinci Resolve 已退出，正在执行系统关机…'; "
        "shutdown.exe /s /t 0; "
        "if ($LASTEXITCODE -ne 0) {{ Write-Host 'Windows 未能启动关机流程。'; "
        "Write-Host ''; Write-Host '按任意键关闭此窗口。'; $null = [Console]::ReadKey($true) }}"
    ).format(SCRIPT_NAME, AUTHOR, HOMEPAGE, RESULT)
    flags = (getattr(subprocess, "CREATE_NEW_CONSOLE", 0) |
             getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | 0x01000000)
    try:
        subprocess.Popen(["powershell.exe", "-NoProfile", "-Command", command], creationflags=flags)
    except OSError:
        subprocess.Popen(["powershell.exe", "-NoProfile", "-Command", command],
                         creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0))


def _start_macos_countdown():
    # Write a short-lived helper because Terminal needs a persistent interactive shell.
    helper_path = os.path.join(tempfile.gettempdir(), "davinci_render_shutdown_{}.sh".format(os.getpid()))
    q = shlex.quote
    lines = [
        "#!/bin/bash",
        "rm -f \"$0\"",
        "printf '%s\\n' '========================================'",
        "printf '%s\\n' {}".format(q(SCRIPT_NAME)),
        "printf '%s\\n' {}".format(q("作者：" + AUTHOR)),
        "printf '%s\\n' {}".format(q("主页：" + HOMEPAGE)),
        "printf '%s\\n\\n' '========================================'",
        "printf '%s\\n' 'DaVinci Resolve 渲染作业已结束。'",
        "printf '%s\\n' {}".format(q("结果：" + RESULT)),
        "printf '%s\\n\\n' '倒计时期间按任意键可取消自动关机。'",
        "for ((i=30; i>=1; i--)); do",
        "  printf '\\r剩余%2d秒  ' \"$i\"",
        "  if IFS= read -r -n 1 -t 1 key; then",
        "    printf '\\n\\n已取消自动关机。\\n\\n按任意键关闭此窗口。\\n'",
        "    IFS= read -r -n 1 key",
        "    exit 0",
        "  fi",
        "  if [ \"$i\" -eq 10 ]; then",
        "    printf '\\n\\n正在请求 DaVinci Resolve 安全退出…\\n'",
        "    /usr/bin/osascript -e 'tell application \"DaVinci Resolve\" to quit' >/dev/null 2>&1",
        "    for ((j=0; j<10; j++)); do",
        "      if ! /usr/bin/pgrep -x Resolve >/dev/null 2>&1; then break; fi",
        "      /bin/sleep 1",
        "    done",
        "    if /usr/bin/pgrep -x Resolve >/dev/null 2>&1; then",
        "      printf '%s\\n' 'DaVinci Resolve 未正常退出，正在强制结束 Resolve 进程…'",
        "      /usr/bin/pkill -KILL -x Resolve",
        "    fi",
        "  fi",
        "done",
        "printf '\\n\\n正在请求 macOS 关机…\\n'",
        "/usr/bin/osascript -e 'tell application \"System Events\" to shut down'",
        "if [ $? -ne 0 ]; then",
        "  printf '%s\\n\\n' 'macOS 未能启动关机流程。请检查自动化权限。'",
        "  printf '%s\\n' '按任意键关闭此窗口。'",
        "  IFS= read -r -n 1 key",
        "fi",
    ]
    with io.open(helper_path, "w", encoding="utf-8") as helper:
        helper.write("\n".join(lines) + "\n")
    os.chmod(helper_path, 0o700)
    applescript = (
        'tell application "Terminal" to do script "bash " & quoted form of "{}"\n'
        'tell application "Terminal" to activate'
    ).format(helper_path.replace('"', '\\"'))
    subprocess.Popen(["/usr/bin/osascript", "-e", applescript])


_log_result(RESULT)
try:
    if sys.platform == "win32":
        _start_windows_countdown()
    elif sys.platform == "darwin":
        _start_macos_countdown()
    else:
        print("{}：当前系统暂不支持自动倒计时和关机。".format(SCRIPT_NAME))
except Exception as exc:
    print("{}：启动倒计时失败（{}）。".format(SCRIPT_NAME, type(exc).__name__))
