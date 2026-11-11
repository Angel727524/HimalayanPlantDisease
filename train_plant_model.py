
import json
import math
from pathlib import Path
from collections import Counter

import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight


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

INITIAL_EPOCHS = 20
FINE_TUNE_EPOCHS = 15

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
# NORMALIZE NAMES
# ==========================================

def normalize_name(name):
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


# ==========================================
# COLLECT IMAGES
# ==========================================

def collect_images():

    paths = []
    labels = []

    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_DIR}"
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
                f"Missing folder: {plant}"
            )

        images = [
            p for p in folder.rglob("*")
            if p.is_file()
            and p.suffix.lower() in IMAGE_EXTENSIONS
        ]

        print(f"{plant}: {len(images)} images")

        if len(images) < 2:
            raise ValueError(
                f"Not enough images for {plant}"
            )

        for image in images:
            paths.append(str(image))
            labels.append(index)

    return paths, labels


# ==========================================
# LOAD IMAGE
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
# PREPARE DATASETS
# ==========================================

def create_datasets(paths, labels):

    train_paths, val_paths, train_labels, val_labels = (
        train_test_split(
            paths,
            labels,
            test_size=0.2,
            random_state=42,
            stratify=labels
        )
    )

    classes = np.unique(train_labels)

    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=np.array(train_labels)
    )

    class_weights = {
        int(class_id): float(weight)
        for class_id, weight in zip(classes, weights)
    }

    print("\nCLASS WEIGHTS")
    for class_id, weight in class_weights.items():
        print(
            f"{PLANT_CLASSES[class_id]}: "
            f"{weight:.3f}"
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
    train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)

    val_dataset = tf.data.Dataset.from_tensor_slices(
        (val_paths, val_labels)
    )

    val_dataset = val_dataset.map(
        load_image,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    val_dataset = val_dataset.batch(BATCH_SIZE)
    val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)

    print("\nTraining images:", len(train_paths))
    print("Validation images:", len(val_paths))

    return train_dataset, val_dataset, class_weights


# ==========================================
# BUILD MODEL
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

    augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.08),
        tf.keras.layers.RandomZoom(0.10),
    ], name="augmentation")

    x = augmentation(inputs)

    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

    x = base_model(x, training=False)

    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    x = tf.keras.layers.Dropout(0.4)(x)

    x = tf.keras.layers.Dense(
        256,
        activation="relu"
    )(x)

    x = tf.keras.layers.Dropout(0.3)(x)

    outputs = tf.keras.layers.Dense(
        len(PLANT_CLASSES),
        activation="softmax"
    )(x)

    model = tf.keras.Model(inputs, outputs)

    return model, base_model


# ==========================================
# CALLBACKS
# ==========================================

def get_callbacks():

    return [
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


# ==========================================
# MAIN TRAINING
# ==========================================

def main():

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n" + "=" * 45)
    print("FLORA PLANT IDENTIFICATION")
    print("=" * 45)

    paths, labels = collect_images()

    print("\nTotal images:", len(paths))
    print("Plant categories:", len(PLANT_CLASSES))

    train_dataset, val_dataset, class_weights = (
        create_datasets(paths, labels)
    )

    model, base_model = build_model()

    # --------------------------------------
    # STAGE 1: TRAIN CLASSIFICATION HEAD
    # --------------------------------------

    print("\nSTAGE 1: Training classification head")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.0001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=INITIAL_EPOCHS,
        class_weight=class_weights,
        callbacks=get_callbacks()
    )

    # --------------------------------------
    # STAGE 2: FINE-TUNE BACKBONE
    # --------------------------------------

    print("\nSTAGE 2: Fine-tuning MobileNetV2")

    base_model.trainable = True

    # Keep most pretrained layers frozen.
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    # Batch normalization should remain frozen.
    for layer in base_model.layers:
        if isinstance(
            layer,
            tf.keras.layers.BatchNormalization
        ):
            layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.00001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=FINE_TUNE_EPOCHS,
        class_weight=class_weights,
        callbacks=get_callbacks()
    )

    # --------------------------------------
    # SAVE CLASS NAMES
    # --------------------------------------

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
    print("FLORA PLANT TRAINING FINISHED")
    print("=" * 45)

    print("Model:", MODEL_PATH)
    print("Labels:", LABELS_PATH)

    print(
        "\nImportant: Check validation accuracy "
        "and test with separate real photos."
    )


if __name__ == "__main__":
    main()
