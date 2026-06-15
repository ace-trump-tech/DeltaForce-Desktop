# DeltaForce 手机端 APK 下载工具

本文件夹包含 **DeltaForce-Locker** 项目的**手机端 APK 自动下载脚本**及演示素材。
> 6ICD5b6X5LiK5aSn5a2m5ZCX77yM5L2g5bCx5byA5oyC
---

## ⭐ 如何获取本项目（手机端）

请按照以下三步操作：

1. **⭐ Star**  
   点击本仓库右上角的 **Star** 按钮，申请自己的使用权限。

2. **⑂ Fork**  
   点击 **Fork** 按钮，将本仓库复制到你自己的 GitHub 账号下，不然无法进行修改。

3. **⬇️ Download**  
   在你自己 Fork 后的仓库页面，点击 **Code → Download ZIP** 下载压缩包。  

> 💡 下载解压后，手机端代码位于 `Mobile/` 文件夹。请根据本 README 的指引下载 APK。

---

## 📱 功能说明

- 提供 Python 脚本 `download_apk.py`，用于从 **Hugging Face** 自动下载 `Locker_Android.apk`（手机端辅助程序）。
- 包含演示素材：`demo.png`（操作流程图）、`demo_video.gif` / `demo_video.mp4`（功能演示视频）。
- APK 安装后，可在 Android 设备上演示**画面吸附 / 模拟触摸输入**效果（仅供学习）。

---

## 🚀 使用方法

### 1️⃣ 环境准备

- 操作系统：Windows / macOS / Linux
- Python 版本：3.6 及以上
- 网络环境：能够正常访问 Hugging Face（如无法访问，请配置代理或使用镜像）

### 2️⃣ 安装依赖

打开终端（命令提示符 / PowerShell / Terminal），进入本文件夹（`Mobile/`），执行：

```bash
pip install requests tqdm
```

- `requests`：用于发送 HTTP 请求下载文件
- `tqdm`：显示下载进度条

### 3️⃣ 运行下载脚本

```bash
python download_apk.py
```

脚本将自动执行以下操作：
- 从 Hugging Face 指定地址下载 `Locker_Android.apk`
- 显示实时下载进度
- 下载完成后，APK 文件保存在当前目录下，文件名为 `Locker_Android.apk`

### 4️⃣ 安装 APK 到手机

- 将下载好的 `Locker_Android.apk` 传输至 Android 手机。
- 在手机设置中允许“安装未知来源应用”。
- 点击 APK 文件完成安装。

---

## 🎮 手机端使用说明

安装并打开 APP 后，请按以下步骤操作：

1. **授予悬浮窗权限**：应用会提示开启，请前往系统设置允许。
2. **开启无障碍服务**：根据应用内指引，在系统设置中启用本应用的无障碍服务（用于模拟触摸）。
3. **进入游戏**：《三角洲行动》手机版。
4. **启动辅助**：点击悬浮窗上的“开始”按钮，应用会自动识别画面中的目标并模拟触摸滑动。
5. **调整参数**：可通过悬浮窗菜单调节灵敏度、平滑度等。

> 详细演示效果请观看 `demo_video.gif` 或 `demo_video.mp4`。

---

## 🔧 自定义下载地址

如果你需要修改 APK 的下载源，请编辑 `download_apk.py`，找到以下变量并替换：

```python
APK_URL = "https://huggingface.co/your-repo/resolve/main/Locker_Android.apk"
```

保存后重新运行脚本即可。

---

## ❓ 常见问题

### Q1: 运行 `download_apk.py` 提示 `ModuleNotFoundError: No module named 'requests'`

**A**: 请执行 `pip install requests tqdm` 安装所需依赖。

### Q2: 下载速度很慢或超时

**A**: 
- 检查网络连接，尝试切换网络环境。
- 手动复制 `APK_URL` 到浏览器下载，然后手动传输至手机。

### Q3: 安装 APK 时提示“解析错误”

**A**: 
- 确保 APK 文件下载完整（检查文件大小）。
- 确认 Android 系统版本为 7.0 或更高。
- 尝试重新下载。

### Q4: 手机端应用启动后无反应

**A**: 
- 确保已授予悬浮窗和无障碍权限。
- 重启应用或手机。
- 检查是否与其他辅助工具冲突。

### Q5: 演示视频无法播放

**A**: 
- `demo_video.gif` 和 `demo_video.mp4` 均为标准格式，请使用支持该格式的图片/视频查看器。
- 如需在线观看，可访问主仓库的 README 中的链接。

---

## 📂 项目文件说明

| 文件 | 说明 |
|------|------|
| `download_apk.py` | APK 自动下载脚本 |
| `demo.png` | Star → Fork → Download 操作流程图 |
| `demo_video.gif` | 功能演示动画（GIF 格式） |
| `demo_video.mp4` | 功能演示视频（MP4 格式） |
| `README.md` | 本说明文档 |

---

## 🔗 相关链接

- 主项目 README：[DeltaForce-OBS-Locker](https://github.com/ace-trump-tech/DeltaForce-OBS-Locker)
- 电脑端项目：[Desktop 端 README](https://github.com/ace-trump-tech/DeltaForce-Locker/blob/main/Desktop/README.md)

---

## 📄 许可证

[MIT License](https://opensource.org/licenses/MIT) —— 仅供学习，禁止商业使用。

*最后更新：2026-06-15*
