import os
import shutil

SOURCE_DIR = "NYPL demo sample photos"
ASSETS_DIR = "assets/sample_images"

MAPPING = {
    "01_pigeon.jpg": "istockphoto-636191406-1024x1024.jpg",
    "02_squirrel.jpg": "istockphoto-1667398983-1024x1024.jpg",
    "03_mouse.jpg": "istockphoto-1287501116-1024x1024.jpg",
    "04_pedestrians.jpg": "istockphoto-1403086073-1024x1024.jpg",
}


def seed():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    for dest_name, src_name in MAPPING.items():
        src = os.path.join(SOURCE_DIR, src_name)
        dst = os.path.join(ASSETS_DIR, dest_name)
        print(f"[SEED] copying {src_name} -> {dest_name} ...")
        try:
            shutil.copy2(src, dst)
            size_kb = os.path.getsize(dst) / 1024
            print(f"[SEED] ok: {dest_name} ({size_kb:.1f} KB)")
        except Exception as e:
            print(f"[SEED] fail: {dest_name} - {e}")


if __name__ == "__main__":
    seed()
