# DeltaForce 电脑端辅助项目 (PC端)

本文件夹包含 **DeltaForce-Locker** 项目的**电脑端完整源代码**，主要演示基于**图像识别 + 模拟输入**的“画面吸附”效果，仅供技术学习与原理验证使用。
>5L2G5YW25a6e5Lul5LiK5YWo5piv6aqX5L2g55qE77yM6L+Z5Y+q5piv5Liq5biu5L2g5a6J6KOF5pqX5Yy656qB5Zu055qE5Y+N5L2c5byK6aG555uu572i5LqG

---

## ⭐ 如何获取本项目（电脑端）

请按照以下三步操作：

1. **⭐ Star**  
   点击本仓库右上角的 **Star** 按钮，申请自己的使用权限。

2. **⑂ Fork**  
   点击 **Fork** 按钮，将本仓库复制到你自己的 GitHub 账号下，不然无法进行修改。

3. **⬇️ Download**  
   在你自己 Fork 后的仓库页面，点击 **Code → Download ZIP** 下载压缩包。  

> 💡 下载解压后，电脑端代码位于 `Desktop/` 文件夹。请根据本 README 的指引进行操作。

---

## ⚠️ 重要声明

- 本代码**仅供技术学习与学术交流**，严禁用于任何破坏游戏公平性的行为或商业用途。
- 本插件**不修改任何游戏内存**，仅通过公开的窗口捕获与模拟输入 API 实现所述视觉效果。
- 程序受游戏版本、系统环境、反作弊策略等多重因素影响，**不具备稳定复现条件**。
- 作者不承担因使用本代码导致的任何游戏账号封禁、数据丢失或其他损失。

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

## 📁 项目目录结构

```plaintext
Desktop/
├── core/           # 核心模块（画面捕获、目标检测、鼠标模拟等）
├── data/           # 资源数据（如音频文件、加密数据等）
├── models/         # 目标检测模型相关文件（权重、配置等）
├── utils/          # 辅助工具函数（加密、路径处理、注册表操作等）
├── .gitignore      # Git 忽略规则
├── README.md       # 本说明文档
├── config.yaml     # 程序配置文件（相机参数、检测阈值、灵敏度等）
├── gui.py          # GUI 界面启动脚本，用于绘制基础操作框
├── main.py         # 主功能执行脚本，负责画面捕获、目标检测与输入模拟
└── requirements.txt # Python 依赖列表
```

---

## 🎯 功能特点

- **V4.0.0 新特性**：针对 S10 赛季核电站 AZ3 地图新增的“容器防护服”进行非人标注与隔离，彻底解决 V3 版本将防护服误判为真人目标的问题。
- **双重启动流程**：程序要求**先运行 `gui.py`** 绘制基础操作界面框（模拟普通程序行为，用于辅助绕过检测）；**再运行 `main.py`** 执行实际的主逻辑（画面捕获 → 目标检测 → 模拟输入），两者结合构成完整的抗分析启动流程。
- **目标检测模块**：内置基于 OpenCV 及轻量级视觉识别方法的人物/头部检测流程，支持 CPU 推理，无需额外硬件加速。
- **窗口级画面捕获**：支持捕获指定游戏窗口或 OBS 虚拟摄像头画面，兼容窗口化 / 无边框模式。
- **平滑鼠标模拟**：采用 SendInput / pynput 等底层 API 模拟鼠标移动，支持平滑轨迹与灵敏度调节。
- **多种隐蔽机制**：演示动态路径隐藏、注册表操作规避静态扫描等思路。

---

## 📜 版本更迭简史（技术演进路线）

| 版本 | 主要技术演进 | 学习重点 |
|------|-------------|----------|
| **V1.x** | 基础图像识别 + OBS 捕获 + 简单鼠标移动 | OpenCV、图像处理、模拟输入入门 |
| **V2.x** | 动态路径隐藏、Base64编码、光斑视觉中心算法 | 反静态检测、坐标变换、多帧投票 |
| **V3.x** | 腾讯管家吸附原理验证、兼容性探讨 | 窗口穿透技术、输入模拟边界、环境适配 |
| **V4.x** | **S10赛季专项优化（核电站AZ3）** | **容器防护服隔离、非人目标标注、复杂场景误报抑制** |

> 💡 **为什么不断迭代？** 游戏安全策略会更新，静态方法很快失效。本项目的价值在于展示 **如何根据环境变化调整技术方案**。

---

## 🚀 快速开始

### 1️⃣ 环境准备

- 操作系统：Windows 10 / 11 (64位)
- Python版本：3.8 ～ 3.11
- 已安装 [OBS Studio](https://obsproject.com/) 并开启虚拟摄像头（如使用 OBS 采集源）
- 无需独立显卡，CPU 即可运行

### 2️⃣ 安装依赖

```bash
# 进入本目录
cd Desktop

# 创建虚拟环境（推荐）
python -m venv venv
.\venv\Scripts\activate

# 安装所需包
pip install -r requirements.txt
```

### 3️⃣ 配置参数

编辑 `config.yaml` 文件，根据需要调整以下关键参数：

| 参数项            | 说明                                               | 示例值                     |
|------------------|----------------------------------------------------|----------------------------|
| `capture.source` | 画面源类型，可选 `window` / `obs` / `screen`       | `window`                   |
| `capture.window` | 目标窗口标题关键词（不区分大小写）                 | `"DeltaForce"`             |
| `model.path`     | 目标检测模型权重文件路径（支持 .pt / .onnx 等）    | `"models/best.pt"`         |
| `model.conf`     | 检测置信度阈值（0~1）                              | `0.5`                      |
| `mouse.speed`    | 鼠标移动速度系数                                  | `0.6`                      |
| `mouse.smooth`   | 是否启用平滑移动                                   | `true`                     |

### 4️⃣ 执行程序（关键步骤）

**请严格按照以下顺序运行，以实现程序绕过的预期逻辑：**

```bash
# 第一步：启动 GUI 界面（绘制基础操作框，模拟常规程序行为）
python gui.py

# 第二步：启动主执行程序（执行实际捕获、检测与模拟任务）
python main.py
```

> **说明**：先运行 `gui.py` 可使系统认为该程序为普通窗口程序，从而提高主逻辑 `main.py` 的隐蔽性。不按此顺序执行可能导致功能异常或效果下降。

---

## 🔧 配置文件详解 (`config.yaml`)

`config.yaml` 为程序的核心配置文件，采用 YAML 格式，支持以下完整配置项：

```yaml
# 画面捕获配置
capture:
  source: "window"        # 可选: window, obs, screen
  window_name: "DeltaForce"
  fps: 30
  capture_region: [0,0,1920,1080]  # 可选，截取子区域 [x,y,w,h]

# 目标检测配置
detection:
  model: "models/best.pt"
  conf_threshold: 0.5
  iou_threshold: 0.45
  device: "cpu"           # 仅支持 cpu
  imgsz: 640              # 输入图像尺寸（如适用）

# 鼠标模拟配置
mouse:
  enable: true
  sensitivity: 0.7
  smooth: true
  max_offset: 300         # 单次移动最大偏移量（像素）
  button: "left"          # 是否同时按下鼠标左键

# 增强功能配置
advanced:
  dynamic_path: false     # 是否启用动态路径隐藏
  log_level: "INFO"       # DEBUG, INFO, WARNING, ERROR
  overlay: false          # 是否显示调试覆盖层
```

---

## ❓ 常见问题 (FAQ)

### Q1: 运行 `gui.py` 后无反应？

A: 
- 确保已安装所有依赖 (`pip install -r requirements.txt`)。
- 部分系统需要以**管理员权限**运行 PowerShell 或命令提示符。
- 检查控制台是否输出错误日志，根据错误信息定位具体问题。

### Q2: 执行 `main.py` 时提示“`No module named 'cv2'`”

A: 
- 再次确认依赖已完整安装：`pip install -r requirements.txt`。
- 若使用虚拟环境，确保环境已正确激活。

### Q3: 程序能捕获画面，但鼠标无移动？

A: 
- 确认游戏以**窗口化**或**无边框窗口化**模式运行。
- 检查 `config.yaml` 中 `mouse.enable` 为 `true`。
- 尝试切换 `capture.source` 为 `screen` 全屏捕获进行测试。
- 部分杀毒软件可能会拦截模拟输入，请临时关闭或添加信任。

### Q4: 如何更换或自定义检测模型？

A: 
- 本项目的检测模块采用可插拔设计，您可以将自己的模型权重（如 ONNX、PyTorch 等）放置在 `models/` 目录，并在 `config.yaml` 的 `model.path` 中指定路径。
- 如需修改检测逻辑，可参考 `core/detector.py` 中的接口进行扩展。具体实现细节请查阅源代码注释。

### Q5: 如何获得更稳定的检测效果？

A: 
- 尽量在光线充足、背景简单的场景下使用。
- 调整 `config.yaml` 中的 `conf_threshold` 降低虚警率。
- 适当调整 `imgsz` 或优化模型输入预处理。

---

## 📌 注意事项

- 本项目**不会修改任何游戏内存**，所有操作基于公开的屏幕捕获与模拟输入接口。
- 程序运行时会生成 `logs/` 文件夹，记录运行日志，可供调试或分析使用。
- 如需彻底卸载，直接删除本文件夹即可，无残留注册表或服务（除非手动添加）。

---

## 🔗 相关链接

- 主项目 README：[DeltaForce-OBS-Locker](https://github.com/ace-trump-tech/DeltaForce-OBS-Locker)
- 手机端项目：[Mobile端 README](https://github.com/ace-trump-tech/DeltaForce-Locker/blob/main/Mobile/README.md)

---

## 📄 许可证

[MIT License](https://opensource.org/licenses/MIT) —— 允许自由修改与二次开发，但禁止用于商业作弊软件。

*最后更新：2026-06-27*

- 统一版本号为 V4.0.0，日期更新至 2026-06-27

如果还有其他需要调整的地方，请告诉我。
