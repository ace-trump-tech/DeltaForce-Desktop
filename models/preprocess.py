from typing import Tuple
import numpy as np


class Preprocessor:
    """输入图像的预处理：缩放、归一化、格式转换"""

    def __init__(self, input_size: Tuple[int, int] = (640, 640), mean=(0.485, 0.456, 0.406),
                 std=(0.229, 0.224, 0.225), bgr_to_rgb: bool = True):
        self.input_w, self.input_h = input_size
        self.mean = np.array(mean, dtype=np.float32).reshape(1, 1, 3)
        self.std = np.array(std, dtype=np.float32).reshape(1, 1, 3)
        self.bgr_to_rgb = bgr_to_rgb

    def letterbox(self, img: np.ndarray) -> Tuple[np.ndarray, float, Tuple[int, int]]:
        """等比例缩放并填充至 input_size，返回 (img_pad, ratio, pad)。"""
        h, w = img.shape[:2]
        r = min(self.input_w / w, self.input_h / h)
        new_w, new_h = int(w * r), int(h * r)
        dw = self.input_w - new_w
        dh = self.input_h - new_h
        top, left = dh // 2, dw // 2
        bottom, right = dh - top, dw - left
        resized = np.pad(
            img,
            ((top, bottom), (left, right), (0, 0)),
            mode="constant",
            constant_values=114,
        )
        return resized, r, (left, top)

    def __call__(self, img: np.ndarray) -> np.ndarray:
        """完整预处理流水线：letterbox -> BGR2RGB -> normalize -> HWC2CHW。"""
        img_pad, ratio, pad = self.letterbox(img)
        img_pad = img_pad.astype(np.float32) / 255.0
        if self.bgr_to_rgb:
            img_pad = img_pad[..., ::-1]
        img_pad = (img_pad - self.mean) / self.std
        img_pad = img_pad.transpose(2, 0, 1)  # HWC -> CHW
        return np.ascontiguousarray(img_pad[np.newaxis, ...])
