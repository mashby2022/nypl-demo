import cv2
import gradio as gr
import numpy as np

# Import the decoupled classes and config from our refactored app.py
from app import VisionEngine, FrameRenderer, DOMAIN_CONFIG

# 1. Initialize the engine once globally so it doesn't reload the model on every click
print("[SYSTEM] Booting Vision Engine...")
engine = VisionEngine(DOMAIN_CONFIG)

def process_upload(input_image):
    """Handles the drag-and-drop image, runs the pipeline, and returns the annotated frame."""
    if input_image is None:
        return None
        
    # Gradio provides images in RGB, but OpenCV/our pipeline uses BGR. 
    frame_bgr = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)
    
    # 2. Run the pure inference API
    detections, latency = engine.analyze_frame(frame_bgr)
    
    # 3. Apply the semantic rendering and privacy masking
    FrameRenderer.render(frame_bgr, detections, DOMAIN_CONFIG["PRIVACY"])
    FrameRenderer.draw_hud(frame_bgr, "web_upload.jpg", 1, 1, latency)
    
    # Convert back to RGB for the web browser
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    
    return frame_rgb

# ==========================================
# Build the Drag-and-Drop Interface
# ==========================================
demo = gr.Interface(
    fn=process_upload,
    inputs=gr.Image(label="Drag & Drop Urban Scene Here"),
    outputs=gr.Image(label="Live Telemetry & Privacy Output"),
    title="NYC Wildlife & Privacy CV Engine",
    description=(
        "**Portfolio Demo:** Upload a street-level photo. The underlying engine runs a generic "
        "detection model but uses a custom presentation layer to map generic classes into a "
        "municipal tracking narrative (e.g., Bird → Pigeon) while applying real-time, dynamic "
        "Gaussian blurring to all pedestrians for data governance."
    ),
    allow_flagging="never",
    theme=gr.themes.Default(primary_hue="blue", neutral_hue="slate")
)

if __name__ == "__main__":
    demo.launch(share=False) # Set share=True if you need a public URL for your 10-minute presentation