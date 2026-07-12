import os
import sys
import time

import cv2
import numpy as np
import streamlit as st

# Reuse the actual pipeline classes from the repo root instead of duplicating them.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import VisionEngine, FrameRenderer, DOMAIN_CONFIG  # noqa: E402

st.set_page_config(page_title="NYC Wildlife & Privacy CV Engine", page_icon="🐦", layout="centered")


@st.cache_resource
def load_engine():
    return VisionEngine(DOMAIN_CONFIG)


SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sample_images")
SAMPLE_IMAGES = sorted(
    f for f in os.listdir(SAMPLE_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))
) if os.path.isdir(SAMPLE_DIR) else []

st.title("NYC Wildlife & Privacy CV Engine")
st.markdown(
    "A learning resource from the WTX x NYPL *\"Vibe Coding\"* panel. Upload a street-level photo "
    "(or pick a sample below) and a general-purpose YOLOv8 model &mdash; trained on COCO, not on a "
    "custom wildlife dataset &mdash; maps a few of its classes onto an urban-wildlife narrative "
    "(bird &rarr; pigeon, cat/dog &rarr; squirrel proxy, mouse &rarr; rat alert) while applying "
    "real-time Gaussian blurring to any detected people for privacy.\n\n"
    "Full source, README, and an honest write-up of the model's limits: "
    "[github.com/mashby2022/nypl-demo](https://github.com/mashby2022/nypl-demo)"
)

engine = load_engine()

col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader("Upload your own photo", type=["jpg", "jpeg", "png"])
with col2:
    sample_choice = st.selectbox("...or try a sample image", ["(none)"] + SAMPLE_IMAGES)

frame_bgr = None
source_name = None

if uploaded is not None:
    file_bytes = np.frombuffer(uploaded.read(), np.uint8)
    frame_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    source_name = uploaded.name
elif sample_choice != "(none)":
    frame_bgr = cv2.imread(os.path.join(SAMPLE_DIR, sample_choice))
    source_name = sample_choice

if frame_bgr is not None:
    with st.spinner("Running inference..."):
        t0 = time.perf_counter()
        detections, latency_ms = engine.analyze_frame(frame_bgr)
        FrameRenderer.render(frame_bgr, detections, DOMAIN_CONFIG["PRIVACY"], DOMAIN_CONFIG["THEME"])
        FrameRenderer.draw_hud(frame_bgr, source_name, 1, 1, latency_ms, DOMAIN_CONFIG["THEME"])

    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    st.image(frame_rgb, caption=f"{source_name} — {latency_ms:.1f} ms inference", use_container_width=True)

    if detections:
        st.subheader("Telemetry")
        for det in detections:
            st.write(f"**{det['label']}** — raw class `{det['class']}`, confidence {det['confidence']:.2f}")
    else:
        st.info("No detections above the 0.40 confidence threshold for this image.")
else:
    st.caption("Upload a photo or pick a sample to see the pipeline run.")
