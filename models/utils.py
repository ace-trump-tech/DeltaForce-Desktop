import numpy as np

def xywh2xyxy(boxes: np.ndarray) -> np.ndarray:
    """[x, y, w, h] -> [x1, y1, x2, y2]"""
    out = np.copy(boxes)
    out[..., 0] = boxes[..., 0] - boxes[..., 2] / 2
    out[..., 1] = boxes[..., 1] - boxes[..., 3] / 2
    out[..., 2] = boxes[..., 0] + boxes[..., 2] / 2
    out[..., 3] = boxes[..., 1] + boxes[..., 3] / 2
    return out

def xyxy2xywh(boxes: np.ndarray) -> np.ndarray:
    """[x1, y1, x2, y2] -> [x, y, w, h]"""
    out = np.copy(boxes)
    out[..., 0] = (boxes[..., 0] + boxes[..., 2]) / 2
    out[..., 1] = (boxes[..., 1] + boxes[..., 3]) / 2
    out[..., 2] = boxes[..., 2] - boxes[..., 0]
    out[..., 3] = boxes[..., 3] - boxes[..., 1]
    return out


def scale_coords(coords: np.ndarray, src_shape, dst_shape) -> np.ndarray:
    """将预测坐标从 src_shape 缩放到 dst_shape。"""
    gain = min(src_shape[0] / dst_shape[0], src_shape[1] / dst_shape[1])
    pad_x = (src_shape[1] - dst_shape[1] * gain) / 2
    pad_y = (src_shape[0] - dst_shape[0] * gain) / 2
    out = np.copy(coords)
    out[..., 0] = (coords[..., 0] - pad_x) / gain
    out[..., 1] = (coords[..., 1] - pad_y) / gain
    out[..., 2] = (coords[..., 2] - pad_x) / gain
    out[..., 3] = (coords[..., 3] - pad_y) / gain
    np.clip(out[..., :4], 0, max(dst_shape), out=out[..., :4])
    return out


def nms(boxes: np.ndarray, scores: np.ndarray, iou_thres: float = 0.45) -> np.ndarray:
    """非极大值抑制 (NumPy 实现)，返回保留的索引列表。"""
    if boxes.shape[0] == 0:
        return np.array([], dtype=np.int32)

    x1, y1 = boxes[:, 0], boxes[:, 1]
    x2, y2 = boxes[:, 2], boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        iou = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(iou <= iou_thres)[0]
        order = order[inds + 1]

    return np.array(keep, dtype=np.int32)
