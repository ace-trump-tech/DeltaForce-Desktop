from pathlib import Path
from typing import Tuple, List
import numpy as np
from .__base_model import BaseModel
from .preprocess import Preprocessor
from .postprocess import Postprocessor


class Detector(BaseModel):
    """目标检测 / 骨骼识别模型：加载、推理、后处理一体化"""

    def __init__(self, weights_path: str = "", device: str = "cpu",
                 conf_thres: float = 0.5, iou_thres: float = 0.45,
                 input_size: Tuple[int, int] = (640, 640),
                 class_names: List[str] = None):
        super().__init__(weights_path, device, conf_thres)
        self.preprocessor = Preprocessor(input_size=input_size)
        self.postprocessor = Postprocessor(
            conf_thres=conf_thres, iou_thres=iou_thres,
            max_det=100, class_names=class_names
        )
        self.input_shape = input_size

    def load(self) -> None:
        """加载模型权重。支持 .onnx (ONNX Runtime) 格式和 .pt (暂用 numpy 模拟)。"""
        if self.weights_path and self.weights_path.exists():
            if self.weights_path.suffix == ".onnx":
                try:
                    import onnxruntime as ort
                    self.model = ort.InferenceSession(str(self.weights_path))
                except ImportError:
                    raise ImportError("ONNX Runtime not installed. Run: pip install onnxruntime")
            else:
                # 占位：实际部署时替换为对应框架的加载逻辑
                self.model = "placeholder"
            self._loaded = True
        else:
            raise FileNotFoundError(f"Weights file not found: {self.weights_path}")

    def predict(self, x: np.ndarray) -> np.ndarray:
        """执行推理，返回 shape (1, N, 6) 的检测结果 [cx, cy, w, h, conf, cls]."""
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call .load() first.")
        # 占位：模拟输出一批检测框
        return np.random.randn(1, 10, 6).astype(np.float32)

    def detect(self, img: np.ndarray) -> List[dict]:
        """完整检测流水线：预处理 -> 推理 -> 后处理，返回检测结果列表。"""
        h, w = img.shape[:2]
        blob = self.preprocessor(img)
        preds = self.predict(blob)
        return self.postprocessor(preds, orig_shape=(h, w), input_shape=self.input_shape)

    @staticmethod
    def from_config(config_path: str = "config.yaml") -> "Detector":
        """从 YAML 配置文件创建 Detector 实例。"""
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        model_cfg = cfg.get("model", {})
        return Detector(
            weights_path=model_cfg.get("weights", "models/weights/your_model_weights.pt"),
            device=model_cfg.get("device", "cpu"),
            conf_thres=model_cfg.get("conf_thres", 0.5),
            iou_thres=model_cfg.get("iou_thres", 0.45),
            input_size=tuple(model_cfg.get("input_size", [640, 640])),
            class_names=model_cfg.get("class_names", ["enemy", "head", "body"]),
        )
