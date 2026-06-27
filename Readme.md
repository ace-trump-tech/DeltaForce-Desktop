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

## 🆕 最新更新（2026-06-27）

- **🎯 S10赛季新地图适配（核电站AZ3）**：针对新地图中新增的“容器防护服”进行了专项隔离处理。此前V3版本模型易将该类防护服误判为真人目标，V4版本中已通过专属特征标注将其单独归类为非人单位，有效消除误触发。

  <div align="center">
    <img src="https://github.com/ace-trump-tech/DeltaForce-Locker/blob/main/Mobile/Protective_suit.jpg?raw=true" alt="核电站AZ3容器防护服样本" width="400">
    <br>
    <em>△ 核电站AZ3地图中的容器防护服（V3版本曾误判为真人）</em>
  </div>

- **🧠 识别逻辑增强**：在视觉识别管线中新增了特定轮廓过滤层，确保容器防护服不再参与目标锁定计算，大幅提升复杂场景下的识别纯净度。

---

## 🎥 功能演示

<div align="center">
  <img src="https://github.com/ace-trump-tech/DeltaForce-Locker/blob/main/Mobile/demo_video.gif?raw=true" alt="手机端功能演示" width="400">
  <br>
  <em>手机端 APK 核心效果（画面吸附 / 模拟输入演示）</em>
</div>

---

## 📱 功能说明

- **V4.0.0 新特性**：针对 S10 赛季核电站 AZ3 地图新增的“容器防护服”进行非人标注与隔离，彻底解决 V3 版本将防护服误判为真人目标的问题。
- 提供 Python 脚本 `download_apk.py`，用于从 **Hugging Face** 自动下载 `Locker_Android.apk`（手机端辅助程序）。
- 包含演示素材：`demo.png`（操作流程图）、`demo_video.gif` / `demo_video.mp4`（功能演示视频）。
- APK 安装后，可在 Android 设备上演示**画面吸附 / 模拟触摸输入**效果（仅供学习）。

---

## 📜 版本更迭简史（技术演进路线）

| 版本 | 主要技术演进 | 学习重点 |
|------|-------------|----------|
| **V1.x** | 基础图像识别 + 简单触摸模拟 | OpenCV、图像处理、模拟输入入门 |
| **V2.x** | 动态路径隐藏、光斑视觉中心算法 | 反静态检测、坐标变换、多帧投票 |
| **V3.x** | 腾讯管家吸附原理验证、兼容性探讨 | 窗口穿透技术、输入模拟边界、环境适配 |
| **V4.x** | **S10赛季专项优化（核电站AZ3）** | **容器防护服隔离、非人目标标注、复杂场景误报抑制** |

> 💡 **为什么不断迭代？** 游戏安全策略会更新，静态方法很快失效。本项目的价值在于展示 **如何根据环境变化调整技术方案**。

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

> 详细演示效果请观看上方 **功能演示** 中的 GIF 动画，或查看 `demo_video.gif` / `demo_video.mp4`。

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
- 如需在线观看，可访问本 README 上方的 **功能演示** 区域，或主仓库 README 中的链接。

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


