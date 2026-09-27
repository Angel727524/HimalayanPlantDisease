import tensorflow as tf
import numpy as np
from pathlib import Path
import sys
sys.path.append(".")
from database import get_database_connection

# =========================
# SETTINGS
# =========================

MODEL_PATH = "models/plant_model.keras"

IMAGE_PATH = "dataset/Rhododendron/Healthy"

IMAGE_SIZE = (224, 224)

# =========================
# FIND AN IMAGE
# =========================

image_folder = Path(IMAGE_PATH)

image_files = list(image_folder.glob("*.jpg"))
image_files += list(image_folder.glob("*.jpeg"))
image_files += list(image_folder.glob("*.png"))

if not image_files:
    print("No image found in:")
    print(image_folder)
    exit()

image_path = image_files[0]

print("Testing image:")
print(image_path)

# =========================
# LOAD MODEL
# =========================

print("\nLoading AI model...")

model = tf.keras.models.load_model(MODEL_PATH)

# =========================
# PLANT NAMES
# =========================

class_names = [
    "Alder",
    "Atis",
    "Blue_Pine",
    "Chir_Pine",
    "Chiraito",
    "Himalayan_Blueberry",
    "Himalayan_Maple",
    "Himalayan_Oak",
    "Himalayan_Raspberry",
    "Jatamasi",
    "Juniper",
    "Kutki",
    "Rhododendron",
    "Timur",
    "Yarsagumba"
]

# =========================
# LOAD IMAGE
# =========================

image = tf.keras.utils.load_img(
    image_path,
    target_size=IMAGE_SIZE
)

image_array = tf.keras.utils.img_to_array(image)

image_array = np.expand_dims(
    image_array,
    axis=0
)

# =========================
# PREDICTION
# =========================

predictions = model.predict(image_array)

predicted_index = np.argmax(predictions[0])

predicted_plant = class_names[predicted_index]

confidence = predictions[0][predicted_index] * 100

# =========================
# RESULT
# =========================

print("\n==============================")
print("AI PREDICTION")
print("==============================")

print("Predicted plant:", predicted_plant)
print(f"Confidence: {confidence:.2f}%")

print("==============================")
print("\nSearching MySQL database...")

connection = get_database_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT plant_name, scientific_name, local_name,
           description, habitat, altitude_range, uses
    FROM plants
    WHERE plant_name = %s
""", (predicted_plant,))

plant = cursor.fetchone()

if plant:
    print("\n==============================")
    print("PLANT INFORMATION")
    print("==============================")

    print("Plant name:", plant[0])
    print("Scientific name:", plant[1])
    print("Local name:", plant[2])
    print("Description:", plant[3])
    print("Habitat:", plant[4])
    print("Altitude:", plant[5])
    print("Uses:", plant[6])

else:
    print("Plant not found in database.")

cursor.close()
connection.close()