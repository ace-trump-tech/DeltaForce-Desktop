from abc import ABC, abstractmethod
from pathlib import Path
import numpy as np


class BaseModel(ABC):
    """所有模型的基类，定义通用接口"""

    def __init__(self, weights_path: str = "", device: str = "cpu", conf_thres: float = 0.5):
        self.weights_path = Path(weights_path) if weights_path else None
        self.device = device
        self.conf_thres = conf_thres
        self.model = None
        self._loaded = False

    @abstractmethod
    def load(self) -> None:
        """加载模型权重。"""
        ...

    @abstractmethod
    def predict(self, x: np.ndarray) -> np.ndarray:
        """执行推理，返回模型原始输出。"""
        ...

    @property
    def loaded(self) -> bool:
        return self._loaded

    def warmup(self, input_shape=(1, 3, 640, 640)) -> None:
        """使用随机数据预热模型（可选）。"""
        dummy = np.random.randn(*input_shape).astype(np.float32)
        _ = self.predict(dummy)
