import os
import shutil
import time
import cv2
import numpy as np
from ultralytics import YOLO

# ==========================================
# CONFIGURATION LAYER
# ==========================================
DOMAIN_CONFIG = {
    "INPUT_DIR": "assets/sample_images",
    "OUTPUT_DIR": "assets/outputs",
    "MODEL_PATH": "yolov8n.pt",
    "CONF_THRESHOLD": 0.40,
    "PRIVACY": {
        "CLASS": "person",
        "LABEL": "PRIVACY MASK",
        "KERNEL_FACTOR": 0.15,  # 15% of bbox width for dynamic blur
        "COLOR": (0, 140, 255)  # Orange
    },
    "THEME": {
        "TEAL": (180, 212, 45),
        "CRIMSON": (59, 59, 212),
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0)
    },
    "LABEL_MAP": {
        "bird": ("NATIVE: Pigeon/Bird", "native"),
        "cat": ("NATIVE: Squirrel (Proxy)", "native"),
        "dog": ("NATIVE: Squirrel (Proxy)", "native"),
        "mouse": ("ALERT: Rat/Mouse", "alert"),
    }
}


def reset_environment(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)


class VisionEngine:
    """Runs YOLO inference and maps raw class names onto the domain's semantic labels."""

    def __init__(self, config):
        self.config = config
        self.model = YOLO(config["MODEL_PATH"])

    def analyze_frame(self, frame):
        t0 = time.perf_counter()
        results = self.model(frame, verbose=False)[0]
        latency_ms = (time.perf_counter() - t0) * 1000

        privacy_cfg = self.config["PRIVACY"]
        label_map = self.config["LABEL_MAP"]
        threshold = self.config["CONF_THRESHOLD"]

        detections = []
        for box in results.boxes:
            conf = float(box.conf[0])
            cls_name = self.model.names[int(box.cls[0])]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if cls_name == privacy_cfg["CLASS"]:
                detections.append({
                    "type": "privacy",
                    "class": cls_name,
                    "raw_class": cls_name,
                    "label": privacy_cfg["LABEL"],
                    "confidence": round(conf, 4),
                    "box": [x1, y1, x2, y2],
                })
                continue

            if cls_name not in label_map or conf <= threshold:
                continue

            label, kind = label_map[cls_name]
            detections.append({
                "type": kind,
                "class": cls_name,
                "raw_class": cls_name,
                "label": label,
                "confidence": round(conf, 4),
                "box": [x1, y1, x2, y2],
            })

        return detections, latency_ms


class FrameRenderer:
    """Draws detections and HUD telemetry onto a frame in place."""

    @staticmethod
    def _draw_box(frame, box, label, color):
        x1, y1, x2, y2 = box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
        cv2.putText(frame, label, (x1, max(y1 - 8, 12)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv2.LINE_AA)

    @staticmethod
    def _apply_privacy_mask(frame, box, privacy_cfg):
        h, w, _ = frame.shape
        x1, y1, x2, y2 = box

        x1 = max(0, min(x1, w - 1))
        x2 = max(0, min(x2, w - 1))
        y1 = max(0, min(y1, h - 1))
        y2 = max(0, min(y2, h - 1))
        if (x2 - x1) <= 0 or (y2 - y1) <= 0:
            return

        roi = frame[y1:y2, x1:x2]
        kernel_size = int((x2 - x1) * privacy_cfg["KERNEL_FACTOR"])
        kernel_size += 1 if kernel_size % 2 == 0 else 0
        kernel_size = max(3, kernel_size)

        frame[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (kernel_size, kernel_size), 0)
        FrameRenderer._draw_box(frame, (x1, y1, x2, y2), privacy_cfg["LABEL"], privacy_cfg["COLOR"])

    @staticmethod
    def render(frame, detections, privacy_cfg, theme=None):
        theme = theme or {"TEAL": (180, 212, 45), "CRIMSON": (59, 59, 212)}
        for det in detections:
            box = det["box"]
            if det["type"] == "privacy":
                FrameRenderer._apply_privacy_mask(frame, box, privacy_cfg)
                continue
            color = theme["CRIMSON"] if det["type"] == "alert" else theme["TEAL"]
            FrameRenderer._draw_box(frame, box, f"{det['label']} {det['confidence']:.2f}", color)

    @staticmethod
    def draw_hud(frame, filename, index, total, latency_ms, theme=None):
        theme = theme or {"WHITE": (255, 255, 255), "BLACK": (0, 0, 0)}
        white, black = theme["WHITE"], theme["BLACK"]
        cv2.rectangle(frame, (0, 0), (520, 115), black, -1)
        cv2.putText(frame, f"FILE: {filename}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, white, 2, cv2.LINE_AA)
        cv2.putText(frame, f"FRAME: {index}/{total}", (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, white, 2, cv2.LINE_AA)
        cv2.putText(frame, f"INFER: {latency_ms:.2f} ms", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, white, 2, cv2.LINE_AA)


def process_image(engine, path, index, total):
    frame = cv2.imread(path)
    if frame is None:
        print(f"[APP] skip: {path} (unreadable)")
        return

    detections, latency_ms = engine.analyze_frame(frame)
    FrameRenderer.render(frame, detections, DOMAIN_CONFIG["PRIVACY"], DOMAIN_CONFIG["THEME"])

    filename = os.path.basename(path)
    FrameRenderer.draw_hud(frame, filename, index, total, latency_ms, DOMAIN_CONFIG["THEME"])

    out_path = os.path.join(DOMAIN_CONFIG["OUTPUT_DIR"], filename)
    cv2.imwrite(out_path, frame)

    cv2.imshow("NYC Wildlife CV", frame)
    cv2.waitKey(0)


def main():
    reset_environment(DOMAIN_CONFIG["OUTPUT_DIR"])
    engine = VisionEngine(DOMAIN_CONFIG)

    images = sorted(
        f for f in os.listdir(DOMAIN_CONFIG["INPUT_DIR"])
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    total = len(images)

    for i, filename in enumerate(images, start=1):
        process_image(engine, os.path.join(DOMAIN_CONFIG["INPUT_DIR"], filename), i, total)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
