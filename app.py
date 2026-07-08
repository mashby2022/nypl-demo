import os
import shutil
import time

import cv2
from ultralytics import YOLO

INPUT_DIR = "assets/sample_images"
OUTPUT_DIR = "assets/outputs"
MODEL_PATH = "yolov8n.pt"
CONF_THRESHOLD = 0.40
BLUR_KERNEL = (99, 99)

TEAL = (180, 212, 45)
CRIMSON = (59, 59, 212)
ORANGE = (0, 140, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

LABEL_MAP = {
    "bird": ("NATIVE: Pigeon/Bird", TEAL),
    "cat": ("NATIVE: Squirrel (Proxy)", TEAL),
    "dog": ("NATIVE: Squirrel (Proxy)", TEAL),
    "mouse": ("ALERT: Rat/Mouse", CRIMSON),
}


def reset_environment():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)


def apply_privacy_mask(frame, box):
    x1, y1, x2, y2 = box
    roi = frame[y1:y2, x1:x2]
    if roi.size == 0:
        return
    frame[y1:y2, x1:x2] = cv2.GaussianBlur(roi, BLUR_KERNEL, 0)
    cv2.rectangle(frame, (x1, y1), (x2, y2), ORANGE, 2)
    cv2.putText(frame, "PRIVACY MASK", (x1, max(y1 - 8, 12)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, ORANGE, 2, cv2.LINE_AA)


def draw_detection(frame, box, label, color):
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, label, (x1, max(y1 - 8, 12)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)


def draw_hud(frame, filename, index, total, latency_ms):
    cv2.rectangle(frame, (0, 0), (360, 72), BLACK, -1)
    cv2.putText(frame, f"FILE: {filename}", (10, 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1, cv2.LINE_AA)
    cv2.putText(frame, f"FRAME: {index}/{total}", (10, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1, cv2.LINE_AA)
    cv2.putText(frame, f"INFER: {latency_ms:.2f} ms", (10, 62),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1, cv2.LINE_AA)


def process_image(model, path, index, total):
    frame = cv2.imread(path)
    if frame is None:
        print(f"[APP] skip: {path} (unreadable)")
        return

    t0 = time.perf_counter()
    results = model(frame, verbose=False)[0]
    latency_ms = (time.perf_counter() - t0) * 1000

    for box in results.boxes:
        conf = float(box.conf[0])
        cls_name = model.names[int(box.cls[0])]
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if cls_name == "person":
            apply_privacy_mask(frame, (x1, y1, x2, y2))
            continue

        if cls_name not in LABEL_MAP or conf <= CONF_THRESHOLD:
            continue

        label, color = LABEL_MAP[cls_name]
        draw_detection(frame, (x1, y1, x2, y2), f"{label} {conf:.2f}", color)

    filename = os.path.basename(path)
    draw_hud(frame, filename, index, total, latency_ms)

    out_path = os.path.join(OUTPUT_DIR, filename)
    cv2.imwrite(out_path, frame)

    cv2.imshow("NYC Wildlife CV", frame)
    cv2.waitKey(0)


def main():
    reset_environment()
    model = YOLO(MODEL_PATH)

    images = sorted(
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    total = len(images)

    for i, filename in enumerate(images, start=1):
        process_image(model, os.path.join(INPUT_DIR, filename), i, total)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
