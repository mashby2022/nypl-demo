# NYC Wildlife CV Demo

A mock computer-vision pipeline that runs YOLOv8 object detection on street-level NYC photos, but semantically relabels generic COCO classes into a wildlife and pest-monitoring narrative.

This demo is engineered to look like a purpose-built, municipal wildlife-tracking system. In reality, it’s a stock detector wearing a clever costume—allowing you to pitch the product UX, data governance, and analytics value without the upfront cost of training custom rodent or avian models.

---

## 🚀 What It Does

The core application (`app.py`) processes four seeded NYC images (a pigeon, a squirrel, a rat, and a crowded crosswalk) through a standard `yolov8n.pt` model. Instead of outputting raw COCO labels, the presentation layer intercepts and remaps the detections to fit a city-management narrative:

### The Semantic Illusion Layer

| Original COCO Class | Remapped Narrative Label | UI Box Color | Context |
| --- | --- | --- | --- |
| `bird` | **NATIVE: Pigeon/Bird** | 🟢 Teal | Standard urban fauna |
| `cat` / `dog` | **NATIVE: Squirrel (Proxy)** | 🟢 Teal | Used to simulate squirrel detections |
| `mouse` | **ALERT: Rat/Mouse** | 🔴 Crimson | High-priority pest monitoring |

### 🔒 Privacy-First Data Governance

Any `person` detection bypasses the wildlife pipeline entirely. Instead, the system applies:

* A heavy **Gaussian blur** directly over the bounding box coordinates.
* An orange **"PRIVACY MASK"** label.

This simulates the real-world anonymization protocols required by municipal data-governance standards before footage can be analyzed or stored.

### 📊 The HUD (Heads-Up Display)

Each processed frame features a sleek, black HUD overlay in the corner displaying:

* Filename & Frame Index
* **Real Inference Latency:** Calculated dynamically via `time.perf_counter()`. *This is the one part of the display that isn’t fabricated!*

---

## 📁 Repository Structure

* **`app.py`**: The main execution script. Steps through the image queue using an OpenCV window, handling the remapping, blurring, and HUD rendering.
* **`seed_assets.py`**: A helper utility that pulls the 4 required sample images from your local iStock/source folder and establishes the baseline environment.
* **`mock_telemetry.py`**: Generates a synthetic, 2,000-row, 12-month CSV dataset of borough- and zip-level "detections." It includes a deliberate summer spike in rat density to give you instant, realistic data to feed into a dashboard or analytics story.
* **`assets/outputs/`**: The directory where final, annotated, and anonymized frames are saved.

---

## 🛠️ Getting Started

### Prerequisites

Make sure you have Python installed along with OpenCV and Ultralytics YOLO:

```bash
pip install opencv-python ultralytics pandas

```

### Running the Demo

1. **Seed your assets** (ensures your source images are in place):
```bash
python seed_assets.py

```


2. **Launch the pipeline**:
```bash
python app.py

```


3. **Interact**: The OpenCV window will display frames one by one. **Press any key** to advance to the next image.
4. **Generate Analytics Data** (Optional): Run the telemetry script to spin up the mock backend dataset for presentations:
```bash
python mock_telemetry.py

```



---

## 💡 Why This Approach?

> **Smoke and mirrors with a purpose.** > Training niche computer vision models for specific urban pests requires thousands of manually labeled images and hours of compute. This demo proves that by combining a lightweight, off-the-shelf model (`yolov8n`) with creative presentation-layer logic, you can effectively demonstrate a high-fidelity product experience, validate the user journey, and showcase data-privacy solutions to stakeholders before writing a single line of custom ML training code.
