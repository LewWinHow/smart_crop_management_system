import os
import cv2
import uuid
import numpy as np
from ultralytics import YOLO
from django.conf import settings

# 全局加载模型（很重要）
model = YOLO(r"C:\Users\xiaoh\Downloads\smart_crop_management_system\ai_model\yolo\best.pt")

def crop_and_save_from_file(image_file, output_folder="oil_palm_tree"):
    """
    直接接收 Django UploadedFile，进行 YOLO 抠图并保存
    返回：相对路径
    """

    # ✅ 1. 读取 Django 文件对象 → numpy
    file_bytes = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return None

    h, w, _ = img.shape

    # ✅ 2. YOLO 推理（直接用 numpy）
    results = model(img)
    boxes = results[0].boxes

    if boxes is None or len(boxes) == 0:
        return None

    # ✅ 3. 找最大框
    max_area = 0
    best_box = None

    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        area = (x2 - x1) * (y2 - y1)

        if area > max_area:
            max_area = area
            best_box = (x1, y1, x2, y2)

    x1, y1, x2, y2 = best_box

    # ✅ 4. 扩大 30%
    dw = (x2 - x1) * 0.3 / 2
    dh = (y2 - y1) * 0.3 / 2

    x1 = int(max(0, x1 - dw))
    y1 = int(max(0, y1 - dh))
    x2 = int(min(w, x2 + dw))
    y2 = int(min(h, y2 + dh))

    # ✅ 5. 裁剪
    cropped = img[y1:y2, x1:x2]

    # ✅ 6. 保存
    save_dir = os.path.join(settings.MEDIA_ROOT, output_folder)
    os.makedirs(save_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.jpg"
    save_path = os.path.join(save_dir, filename)

    cv2.imwrite(save_path, cropped)

    return os.path.join(output_folder, filename).replace("\\", "/")