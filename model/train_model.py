
import json
import math
from pathlib import Path

import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split


# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "plant_model.keras"
LABELS_PATH = MODEL_DIR / "plant_class_names.json"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 20

PLANT_CLASSES = [
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

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


# ==========================================
# NORMALIZE FOLDER NAMES
# ==========================================

def normalize_name(name):
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


# ==========================================
# COLLECT PLANT IMAGES
# ==========================================

def collect_images():

    image_paths = []
    labels = []

    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset folder not found: {DATASET_DIR}"
        )

    folders = {
        normalize_name(folder.name): folder
        for folder in DATASET_DIR.iterdir()
        if folder.is_dir()
    }

    print("\nPLANT IMAGE COUNTS")
    print("-" * 40)

    for index, plant in enumerate(PLANT_CLASSES):

        folder = folders.get(normalize_name(plant))

        if folder is None:
            raise FileNotFoundError(
                f"Missing plant folder: {plant}"
            )

        plant_images = [
            path for path in folder.rglob("*")
            if path.is_file()
            and path.suffix.lower() in IMAGE_EXTENSIONS
        ]

        print(f"{plant}: {len(plant_images)} images")

        if len(plant_images) < 2:
            raise ValueError(
                f"Not enough images for {plant}. "
                "Add at least 2 images."
            )

        for image_path in plant_images:
            image_paths.append(str(image_path))
            labels.append(index)

    return image_paths, labels


# ==========================================
# LOAD AND PREPROCESS IMAGES
# ==========================================

def load_image(path, label):

    image = tf.io.read_file(path)

    image = tf.io.decode_image(
        image,
        channels=3,
        expand_animations=False
    )

    image.set_shape([None, None, 3])

    image = tf.image.resize(
        image,
        IMG_SIZE
    )

    image = tf.cast(image, tf.float32)

    return image, label


# ==========================================
# CREATE TRAINING DATASETS
# ==========================================

def create_datasets(paths, labels):

    number_of_classes = len(PLANT_CLASSES)

    # Ensure the validation set has enough
    # images to represent every plant class.
    total_images = len(paths)

    validation_count = max(
        math.ceil(total_images * 0.2),
        number_of_classes
    )

    if total_images - validation_count < number_of_classes:
        raise ValueError(
            "Not enough images for a reliable "
            "train/validation split."
        )

    train_paths, val_paths, train_labels, val_labels = (
        train_test_split(
            paths,
            labels,
            test_size=validation_count,
            random_state=42,
            stratify=labels
        )
    )

    train_dataset = tf.data.Dataset.from_tensor_slices(
        (train_paths, train_labels)
    )

    train_dataset = train_dataset.shuffle(
        len(train_paths),
        seed=42
    )

    train_dataset = train_dataset.map(
        load_image,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    train_dataset = train_dataset.batch(BATCH_SIZE)

    train_dataset = train_dataset.prefetch(
        tf.data.AUTOTUNE
    )

    val_dataset = tf.data.Dataset.from_tensor_slices(
        (val_paths, val_labels)
    )

    val_dataset = val_dataset.map(
        load_image,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    val_dataset = val_dataset.batch(BATCH_SIZE)

    val_dataset = val_dataset.prefetch(
        tf.data.AUTOTUNE
    )

    return train_dataset, val_dataset


# ==========================================
# BUILD PLANT IDENTIFICATION MODEL
# ==========================================

def build_model():

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet"
    )

    base_model.trainable = False

    inputs = tf.keras.Input(
        shape=(224, 224, 3)
    )

    x = tf.keras.layers.RandomFlip(
        "horizontal"
    )(inputs)

    x = tf.keras.layers.RandomRotation(
        0.08
    )(x)

    x = tf.keras.layers.RandomZoom(
        0.10
    )(x)

    x = tf.keras.applications.mobilenet_v2.preprocess_input(
        x
    )

    x = base_model(
        x,
        training=False
    )

    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    x = tf.keras.layers.Dropout(0.35)(x)

    outputs = tf.keras.layers.Dense(
        len(PLANT_CLASSES),
        activation="softmax"
    )(x)

    model = tf.keras.Model(
        inputs=inputs,
        outputs=outputs
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.0001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


# ==========================================
# TRAIN MODEL
# ==========================================

def main():

    print("\n")
    print("=" * 45)
    print("FLORA PLANT IDENTIFICATION MODEL")
    print("=" * 45)

    paths, labels = collect_images()

    print("\nTotal images:", len(paths))
    print("Total plant classes:", len(PLANT_CLASSES))

    train_dataset, val_dataset = create_datasets(
        paths,
        labels
    )

    model = build_model()

    model.summary()

    callbacks = [

        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        ),

        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(MODEL_PATH),
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=2,
            min_lr=0.000001,
            verbose=1
        )
    ]

    print("\nStarting plant model training...\n")

    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save the exact class order used by the model.
    with open(
        LABELS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            PLANT_CLASSES,
            file,
            indent=4
        )

    print("\n" + "=" * 45)
    print("PLANT MODEL TRAINING COMPLETED")
    print("=" * 45)

    print("Model saved:", MODEL_PATH)
    print("Class names saved:", LABELS_PATH)

    best_accuracy = max(
        history.history["val_accuracy"]
    )

    print(
        "Best validation accuracy:",
        round(best_accuracy * 100, 2),
        "%"
    )


if __name__ == "__main__":
    main()
