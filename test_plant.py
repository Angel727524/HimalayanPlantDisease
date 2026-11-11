
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "plant_model.keras"
LABELS_PATH = BASE_DIR / "models" / "plant_class_names.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

with open(LABELS_PATH, "r", encoding="utf-8") as file:
    classes = json.load(file)


print("\nFLORA PLANT MODEL TEST")
print("=" * 40)

for plant in classes:

    folder = BASE_DIR / "dataset" / plant

    images = [
        p for p in folder.rglob("*")
        if p.is_file()
        and p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not images:
        continue

    # Test one image from each plant.
    image_path = images[0]

    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224))

    array = np.array(image, dtype=np.float32)
    array = np.expand_dims(array, axis=0)

    predictions = model.predict(array, verbose=0)[0]

    index = int(np.argmax(predictions))

    predicted_plant = classes[index]
    confidence = float(predictions[index]) * 100

    print(f"\nActual: {plant}")
    print(f"Predicted: {predicted_plant}")
    print(f"Confidence: {confidence:.2f}%")

print("\nTEST FINISHED")
