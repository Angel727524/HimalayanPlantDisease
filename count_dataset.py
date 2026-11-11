from pathlib import Path
from collections import Counter

print("COUNT DATASET SCRIPT STARTED", flush=True)

# Dataset folder location
DATASET_DIR = Path(__file__).parent / "dataset"

# Supported image formats
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

print("Script location:", Path(__file__).resolve(), flush=True)
print("Dataset location:", DATASET_DIR.resolve(), flush=True)

# Check whether the dataset folder exists
if not DATASET_DIR.exists():
    print("\nERROR: The dataset folder was not found.", flush=True)
    print("Expected location:", DATASET_DIR.resolve(), flush=True)
    raise SystemExit(1)

if not DATASET_DIR.is_dir():
    print("\nERROR: The dataset path is not a folder.", flush=True)
    raise SystemExit(1)

# Counters
total_images = 0
plant_totals = Counter()
disease_totals = Counter()

print("\nHIMALAYAN PLANT DISEASE DATASET REPORT", flush=True)
print("=" * 60, flush=True)

# Get plant folders
plant_folders = sorted(
    folder for folder in DATASET_DIR.iterdir()
    if folder.is_dir()
)

if not plant_folders:
    print("\nWARNING: No plant folders were found inside dataset.", flush=True)

# Count images for each plant and disease
for plant_folder in plant_folders:
    print(f"\nPlant: {plant_folder.name}", flush=True)

    plant_total = 0

    disease_folders = sorted(
        folder for folder in plant_folder.iterdir()
        if folder.is_dir()
    )

    if not disease_folders:
        print("  WARNING: No disease folders found.", flush=True)

    for disease_folder in disease_folders:
        image_files = [
            file for file in disease_folder.rglob("*")
            if file.is_file()
            and file.suffix.lower() in IMAGE_EXTENSIONS
        ]

        image_count = len(image_files)

        print(
            f"  {disease_folder.name}: {image_count} images",
            flush=True
        )

        plant_total += image_count
        disease_totals[disease_folder.name] += image_count

    print(f"  Plant total: {plant_total}", flush=True)

    plant_totals[plant_folder.name] = plant_total
    total_images += plant_total

# Final summary
print("\n" + "=" * 60, flush=True)
print("SUMMARY", flush=True)
print("=" * 60, flush=True)

print("Dataset folder:", DATASET_DIR.resolve(), flush=True)
print("Plant folders:", len(plant_totals), flush=True)
print("Total images:", total_images, flush=True)

print("\nImages per disease category:", flush=True)

if disease_totals:
    for category, count in sorted(disease_totals.items()):
        print(f"{category}: {count}", flush=True)
else:
    print("No disease categories or images were found.", flush=True)

print("\nImages per plant:", flush=True)

for plant, count in sorted(plant_totals.items()):
    print(f"{plant}: {count}", flush=True)

print("\nReport complete.", flush=True)