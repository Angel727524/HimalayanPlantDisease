
from flask import (
    Flask, render_template, request, send_from_directory,
    redirect, url_for, flash
)
from werkzeug.utils import secure_filename

import os
import json
import uuid
import re
import numpy as np
import tensorflow as tf

from database import get_database_connection


# ==================================================
# FLASK CONFIGURATION
# ==================================================

app = Flask(__name__)
app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "flora-himalayan-plant-disease"
)

BASE_DIR = app.root_path

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MODEL_FOLDER = os.path.join(BASE_DIR, "models")
PLANT_IMAGE_FOLDER = os.path.join(BASE_DIR, "static", "plants")

PLANT_MODEL_PATH = os.path.join(
    MODEL_FOLDER, "plant_model.keras"
)

DISEASE_MODEL_PATH = os.path.join(
    MODEL_FOLDER, "disease_model_candidate.keras"
)

PLANT_LABELS_PATH = os.path.join(
    MODEL_FOLDER, "plant_class_names.json"
)

DISEASE_LABELS_PATH = os.path.join(
    MODEL_FOLDER, "disease_class_names_candidate.json"
)

IMAGE_SIZE = (224, 224)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

PLANT_CONFIDENCE_THRESHOLD = 40.0

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLANT_IMAGE_FOLDER, exist_ok=True)


# ==================================================
# PLANT LABELS AND IMAGES
# ==================================================

with open(PLANT_LABELS_PATH, "r", encoding="utf-8") as file:
    PLANT_CLASSES = json.load(file)

if not isinstance(PLANT_CLASSES, list) or not PLANT_CLASSES:
    raise ValueError("Plant labels file is invalid.")


PLANT_IMAGES = {
    "Alder": "Alder.png",
    "Atis": "Atis.png",
    "Blue_Pine": "Blue Pine.png",
    "Chir_Pine": "Chir Pine.png",
    "Chiraito": "Chiraito.png",
    "Himalayan_Blueberry": "Himalayan Blueberry.png",
    "Himalayan_Maple": "Himalayan Maple.png",
    "Himalayan_Oak": "Himalayan Oak.png",
    "Himalayan_Raspberry": "Himalayan Raspberry.png",
    "Jatamasi": "Jatamasi.png",
    "Juniper": "Juniper.png",
    "Kutki": "Kutki.png",
    "Rhododendron": "Rhododendron.png",
    "Timur": "Timur.png",
    "Yarsagumba": "Yarsagumba.png"
}


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def normalize_plant_name(name):
    return str(name).replace("_", " ").strip()


def normalize_disease_name(name):
    """
    Normalize model and database disease names.

    Example:
    'Leaf Spot' and 'Leaf Spot Disease'
    both become 'leaf spot'.
    """

    value = str(name or "").strip().lower()
    value = value.replace("_", " ")
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r" disease$", "", value)

    return value


def get_plant_image(plant_name):

    normalized = normalize_plant_name(plant_name).lower()

    for key, filename in PLANT_IMAGES.items():

        if normalize_plant_name(key).lower() == normalized:

            image_path = os.path.join(
                PLANT_IMAGE_FOLDER,
                filename
            )

            if os.path.isfile(image_path):
                return filename

    return None


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def prepare_image(image_path):

    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMAGE_SIZE,
        color_mode="rgb"
    )

    image_array = tf.keras.utils.img_to_array(image)

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array


# ==================================================
# DATABASE: GET ALL PLANTS
# ==================================================

def get_database_plant_list():

    connection = None
    cursor = None

    try:

        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

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
            ORDER BY plant_name
        """)

        return cursor.fetchall()

    except Exception as error:

        print("Plant list database error:", error)
        return []

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# LOAD PLANT MODEL
# ==================================================

print("\nLoading plant identification model...")

if not os.path.exists(PLANT_MODEL_PATH):
    raise FileNotFoundError(
        f"Plant model not found: {PLANT_MODEL_PATH}"
    )

plant_model = tf.keras.models.load_model(
    PLANT_MODEL_PATH,
    compile=False
)

if plant_model.output_shape[-1] != len(PLANT_CLASSES):
    raise ValueError(
        "Plant model output does not match plant labels."
    )

print("Plant model loaded successfully!")


# ==================================================
# LOAD DISEASE MODEL
# ==================================================

print("\nLoading six-class disease model...")

if not os.path.exists(DISEASE_MODEL_PATH):
    raise FileNotFoundError(
        f"Disease model not found: {DISEASE_MODEL_PATH}"
    )

preprocess = tf.keras.applications.mobilenet_v2.preprocess_input

disease_model = tf.keras.models.load_model(
    DISEASE_MODEL_PATH,
    custom_objects={
        "preprocess_input": preprocess,
        "function": preprocess
    },
    compile=False
)

print("Disease model loaded successfully!")


# ==================================================
# LOAD DISEASE LABELS
# ==================================================

with open(
    DISEASE_LABELS_PATH,
    "r",
    encoding="utf-8"
) as file:
    disease_labels_data = json.load(file)


if isinstance(disease_labels_data, list):
    DISEASE_CLASSES = disease_labels_data

elif isinstance(disease_labels_data, dict):
    DISEASE_CLASSES = (
        disease_labels_data.get("class_names")
        or disease_labels_data.get("classes")
    )

else:
    raise ValueError("Disease labels file has an invalid format.")


EXPECTED_DISEASE_CLASSES = [
    "Healthy",
    "Leaf Spot",
    "Powdery Mildew",
    "Rust",
    "Root Rot",
    "Blight"
]

if DISEASE_CLASSES != EXPECTED_DISEASE_CLASSES:
    raise ValueError(
        f"Unexpected disease label order: {DISEASE_CLASSES}"
    )

if len(DISEASE_CLASSES) != disease_model.output_shape[-1]:
    raise ValueError(
        "Disease labels do not match disease model output."
    )

print("Disease model ready!")
print("Disease classes:", DISEASE_CLASSES)


# ==================================================
# PREDICT PLANT
# ==================================================

def predict_plant(image_path):

    image_array = prepare_image(image_path)

    predictions = plant_model.predict(
        image_array,
        verbose=0
    )[0]

    predicted_index = int(np.argmax(predictions))

    confidence = float(predictions[predicted_index]) * 100

    predicted_plant = PLANT_CLASSES[predicted_index]

    uncertain = confidence < PLANT_CONFIDENCE_THRESHOLD

    return (
        predicted_plant,
        round(confidence, 2),
        uncertain
    )


# ==================================================
# PREDICT DISEASE
# ==================================================

def predict_disease(image_path):

    image_array = prepare_image(image_path)

    predictions = disease_model.predict(
        image_array,
        verbose=0
    )[0]

    predicted_index = int(np.argmax(predictions))

    confidence = float(predictions[predicted_index]) * 100

    predicted_disease = DISEASE_CLASSES[predicted_index]

    return (
        predicted_disease,
        round(confidence, 2)
    )


# ==================================================
# GET PLANT INFORMATION FROM MYSQL
# ==================================================

def get_plant_information(plant_name):

    connection = None
    cursor = None

    try:

        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        search_name = normalize_plant_name(plant_name)

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
            WHERE LOWER(REPLACE(plant_name, '_', ' ')) = LOWER(%s)
            LIMIT 1
        """, (search_name,))

        return cursor.fetchone()

    except Exception as error:

        print("Plant database error:", error)
        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# GET DISEASE INFORMATION BY DISEASE NAME
# ==================================================

def get_disease_information(disease_name):

    """
    The diseases table contains general disease reference records.
    It does not contain a plant_name column.

    Therefore, disease information is matched by disease_name.
    """

    connection = None
    cursor = None

    try:

        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                disease_name,
                disease_type,
                description,
                cause,
                symptoms,
                treatment,
                prevention,
                severity,
                reference_source
            FROM diseases
        """)

        all_diseases = cursor.fetchall()

        wanted_name = normalize_disease_name(disease_name)

        for disease in all_diseases:

            database_name = normalize_disease_name(
                disease.get("disease_name")
            )

            if database_name == wanted_name:
                return disease

        print(
            "No matching disease record found for:",
            disease_name
        )

        return None

    except Exception as error:

        print("Disease database error:", error)
        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def index():

    featured_plants = get_database_plant_list()

    return render_template(
        "index.html",
        featured_plants=featured_plants,
        plant_images=PLANT_IMAGES
    )


# ==================================================
# ABOUT PAGE
# ==================================================

@app.route("/about")
def about():

    return render_template("about.html")


# ==================================================
# PLANT LIBRARY
# ==================================================

@app.route("/plants")
def plants():

    plant_list = get_database_plant_list()

    return render_template(
        "plants.html",
        plants=plant_list,
        plant_images=PLANT_IMAGES
    )


# ==================================================
# PLANT DETAILS
# ==================================================

@app.route("/plants/<path:plant_name>")
def plant_details(plant_name):

    plant = get_plant_information(plant_name)

    if plant is None:
        flash(
            "This plant profile could not be found.",
            "error"
        )
        return redirect(url_for("plants"))

    image_filename = get_plant_image(
        plant["plant_name"]
    )

    # Disease records are general references.
    # The current database schema does not link them to individual plants.
    diseases = []

    template_folder = os.path.join(BASE_DIR, "templates")

    if os.path.isfile(
        os.path.join(template_folder, "plant_details.html")
    ):
        details_template = "plant_details.html"

    elif os.path.isfile(
        os.path.join(template_folder, "plants_details.html")
    ):
        details_template = "plants_details.html"

    else:
        flash(
            "Plant details template could not be found.",
            "error"
        )
        return redirect(url_for("plants"))

    return render_template(
        details_template,
        plant=plant,
        diseases=diseases,
        plant_images=PLANT_IMAGES,
        image_filename=image_filename
    )


# ==================================================
# UPLOADED IMAGE ACCESS
# ==================================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ==================================================
# IMAGE IDENTIFICATION
# ==================================================

@app.route("/upload", methods=["POST"])
def upload():

    file = (
        request.files.get("file")
        or request.files.get("image")
        or request.files.get("plant_image")
    )

    if file is None:
        flash("Please select an image.")
        return redirect(url_for("index"))

    if file.filename == "":
        flash("No image selected.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Only PNG, JPG and JPEG images are allowed.")
        return redirect(url_for("index"))

    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit(".", 1)[1].lower()

    filename = f"{uuid.uuid4().hex}.{extension}"

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    try:

        file.save(image_path)

        # STEP 1: PREDICT PLANT
        predicted_plant, plant_confidence, plant_uncertain = (
            predict_plant(image_path)
        )

        # STEP 2: PREDICT DISEASE
        predicted_disease, disease_confidence = (
            predict_disease(image_path)
        )

        print("\nFLORA ANALYSIS")
        print("Plant:", predicted_plant)
        print("Plant confidence:", plant_confidence)
        print("Plant uncertain:", plant_uncertain)
        print("Disease:", predicted_disease)
        print("Disease confidence:", disease_confidence)

        # STEP 3: GET PLANT INFORMATION WHEN CONFIDENT
        plant = None
        image_filename = None

        if not plant_uncertain:

            plant = get_plant_information(
                predicted_plant
            )

            image_filename = get_plant_image(
                predicted_plant
            )

        # STEP 4: GET MATCHING DISEASE INFORMATION
        healthy_prediction = (
            normalize_disease_name(predicted_disease)
            == "healthy"
        )

        disease_info = None

        if not healthy_prediction:

            disease_info = get_disease_information(
                predicted_disease
            )

        diseases = [disease_info] if disease_info else []

        # STEP 5: DISPLAY RESULTS
        return render_template(
            "result.html",
            predicted_plant=predicted_plant,
            predicted_disease=predicted_disease,
            confidence=plant_confidence,
            plant_confidence=plant_confidence,
            disease_confidence=disease_confidence,
            plant_uncertain=plant_uncertain,
            plant=plant,
            diseases=diseases,
            disease_info=disease_info,
            healthy_prediction=healthy_prediction,
            uploaded_image=filename,
            plant_images=PLANT_IMAGES,
            image_filename=image_filename
        )

    except Exception as error:

        print("Identification error:", error)

        return render_template(
            "result.html",
            error="The image could not be analyzed. Please try another clear JPG or PNG image.",
            uploaded_image=filename
        )


# ==================================================
# ERROR HANDLERS
# ==================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


@app.errorhandler(413)
def file_too_large(error):

    return (
        "Image is too large. Maximum size is 10 MB.",
        413
    )


# ==================================================
# RUN FLASK
# ==================================================

if __name__ == "__main__":

    print("\n------------------------------------")
    print("FLORA - Himalayan Plant Disease System")
    print("------------------------------------")

    print("Plant model: Loaded")
    print("Disease model: Loaded")
    print("Disease categories:", len(DISEASE_CLASSES))
    print("Disease classes:", DISEASE_CLASSES)

    print(
        "Plant confidence threshold:",
        PLANT_CONFIDENCE_THRESHOLD
    )

    print("\nStarting Flask server...")

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
