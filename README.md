# DaVinci Resolve 渲染完成自动关机脚本

本目录包含渲染结束脚本和 Windows、macOS 两个安装脚本。渲染结束脚本会生成桌面结果日志，显示倒计时提示；倒计时期间按任意键可取消自动关机。若未取消，倒计时最后 10 秒会请求 DaVinci Resolve 正常退出；若 Resolve 仍未退出，脚本会强制结束 Resolve 进程，然后继续请求系统关机。强制结束 Resolve 可能丢失未保存内容。

## 文件说明

- `RenderShutdown-hcllmsx.py`：DaVinci Resolve 渲染结束脚本；Resolve 下拉框中会显示 `RenderShutdown-hcllmsx`。
- `安装脚本-forWindows.bat`：Windows 安装脚本。
- `安装脚本-forMac.command`：macOS 安装脚本。

安装时请将 `RenderShutdown-hcllmsx.py` 和对应平台的安装器放在同一个文件夹中。

## Windows 安装

1. 双击 `安装脚本-forWindows.bat`。
2. 安装完成后重启 DaVinci Resolve。
3. 在交付页高级设置中勾选脚本触发，选择 `End`，并选择 `RenderShutdown-hcllmsx`。

## macOS 首次安装

macOS 可以打开 Markdown 文档。可用 Safari 等浏览器、文本编辑器或 VS Code 查看本文件。

1. 将 `RenderShutdown-hcllmsx.py` 和 `安装脚本-forMac.command` 放在同一文件夹。
2. 首次运行前，打开“终端”，输入 `chmod +x `（末尾保留空格），再把 `安装脚本-forMac.command` 拖到终端窗口，按回车执行。这会给安装脚本添加运行权限。
3. 回到 Finder，双击 `安装脚本-forMac.command`。如果 macOS 阻止运行，可按住 Control 键点击该文件并选“打开”；如果系统仍拦截，查看“系统设置 → 隐私与安全性”中的允许选项。
4. 安装完成后重启 DaVinci Resolve。
5. 在交付页高级设置中勾选脚本触发，选择 `End`，并选择 `RenderShutdown-hcllmsx`。

macOS 安装目录为当前用户的：

```text
~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver/
```

## macOS 权限提示

Mac 版会通过 Terminal 请求 DaVinci Resolve 退出，并通过 System Events 请求 macOS 关机。首次使用时，系统可能提示是否允许 Terminal 控制 DaVinci Resolve 或 System Events；请按自己的需要决定是否允许。若拒绝或系统策略阻止关机，终端会显示提示，自动关机可能无法完成。

Mac 版尚未在 macOS 设备上实机验证。若遇到问题，请记录 Resolve 版本、macOS 版本及终端显示的错误信息。

## 结果日志

渲染结束后，脚本会在桌面生成 `DaVinci_Render_Result_日期_时间.txt`，记录完成时间和“渲染作业已结束。”，并附带脚本名称、作者及主页。
