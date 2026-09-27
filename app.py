from flask import Flask, render_template, request
import os
import tensorflow as tf
import numpy as np
from database import get_database_connection

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

MODEL_PATH = "models/plant_model.keras"

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


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_plant(image_path):

    model = tf.keras.models.load_model(MODEL_PATH)

    image = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224)
    )

    image_array = tf.keras.utils.img_to_array(image)

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    predictions = model.predict(image_array, verbose=0)

    predicted_index = np.argmax(predictions[0])

    predicted_plant = class_names[predicted_index]

    confidence = predictions[0][predicted_index] * 100

    return predicted_plant, confidence


def get_plant_information(plant_name):

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            plant_name,
            scientific_name,
            local_name,
            description,
            habitat,
            altitude_range,
            uses
        FROM plants
        WHERE plant_name = %s
    """, (plant_name,))

    plant = cursor.fetchone()

    cursor.close()
    connection.close()

    return plant


def get_diseases(plant_name):

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            d.disease_name,
            d.disease_type,
            d.description,
            d.symptoms,
            d.treatment,
            d.prevention,
            d.severity
        FROM plants p
        JOIN plant_diseases pd
            ON p.plant_id = pd.plant_id
        JOIN diseases d
            ON pd.disease_id = d.disease_id
        WHERE p.plant_name = %s
    """, (plant_name,))

    diseases = cursor.fetchall()

    cursor.close()
    connection.close()

    return diseases


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_image():

    if "plant_image" not in request.files:
        return "No image selected."

    file = request.files["plant_image"]

    if file.filename == "":
        return "No image selected."

    if not allowed_file(file.filename):
        return "Please upload a JPG, JPEG, or PNG image."

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(file_path)

    # AI prediction
    predicted_plant, confidence = predict_plant(file_path)

    # Get plant information
    plant = get_plant_information(predicted_plant)

    # Get diseases
    diseases = get_diseases(predicted_plant)

    return render_template(
        "result.html",
        predicted_plant=predicted_plant,
        confidence=confidence,
        plant=plant,
        diseases=diseases
    )


if __name__ == "__main__":
    app.run(debug=True)