from typing import List, Tuple
import numpy as np
from .utils import xywh2xyxy, scale_coords, nms


class Postprocessor:
    """模型输出结果的后处理：坐标转换、置信度过滤、NMS"""

    def __init__(self, conf_thres: float = 0.5, iou_thres: float = 0.45,
                 max_det: int = 100, class_names: List[str] = None):
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.max_det = max_det
        self.class_names = class_names or ["enemy", "head", "body"]

    def __call__(self, predictions: np.ndarray, orig_shape: Tuple[int, int],
                 input_shape: Tuple[int, int] = (640, 640)
                 ) -> List[dict]:
        """后处理流水线：过滤低置信度 -> xywh2xyxy -> NMS -> 缩放回原图坐标。

        Returns:
            List[dict]: [{"bbox": [x1,y1,x2,y2], "score": float, "class": int, "name": str}, ...]
        """
        if predictions.ndim == 3:
            predictions = predictions[0]  # squeeze batch dim

        mask = predictions[:, 4] >= self.conf_thres
        detections = predictions[mask]
        if detections.shape[0] == 0:
            return []

        boxes = detections[:, :4]
        scores = detections[:, 4]
        class_ids = detections[:, 5].astype(np.int32) if detections.shape[1] > 5 else np.zeros_like(scores, dtype=np.int32)

        boxes_xyxy = xywh2xyxy(boxes)
        boxes_xyxy = scale_coords(boxes_xyxy, input_shape, orig_shape)

        # 按类别分别 NMS
        keep_indices = []
        for cls_id in np.unique(class_ids):
            cls_mask = class_ids == cls_id
            cls_boxes = boxes_xyxy[cls_mask]
            cls_scores = scores[cls_mask]
            cls_keep = nms(cls_boxes, cls_scores, self.iou_thres)
            orig_indices = np.where(cls_mask)[0][cls_keep]
            keep_indices.extend(orig_indices.tolist())

        if len(keep_indices) > self.max_det:
            keep_indices = sorted(keep_indices, key=lambda i: scores[i], reverse=True)[:self.max_det]

        results = []
        for idx in keep_indices:
            results.append({
                "bbox": boxes_xyxy[idx].tolist(),
                "score": float(scores[idx]),
                "class": int(class_ids[idx]),
                "name": self.class_names[class_ids[idx]] if class_ids[idx] < len(self.class_names) else "unknown",
            })
        return results
