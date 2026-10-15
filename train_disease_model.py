
import json
import random
import traceback
from pathlib import Path

import numpy as np
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


# --------------------------------------------------
# 1. PROJECT PATHS AND SETTINGS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "disease_model.keras"
CLASS_NAMES_PATH = MODEL_DIR / "disease_class_names.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 15
SEED = 42

random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)


# --------------------------------------------------
# 2. DISEASE FOLDER NAMES
# --------------------------------------------------

DISEASE_FOLDERS = {
    "healthy": "Healthy",
    "leaf spot": "Leaf Spot",
    "leaf_spot": "Leaf Spot",
    "powdery mildew": "Powdery Mildew",
    "powdery_mildew": "Powdery Mildew",
    "rust": "Rust",
}

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}

CLASS_NAMES = [
    "Healthy",
    "Leaf Spot",
    "Powdery Mildew",
    "Rust",
]


# --------------------------------------------------
# 3. FIND ALL IMAGES IN THE DATASET
# --------------------------------------------------

def collect_images():
    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset folder not found: {DATASET_DIR}"
        )

    image_paths = []
    image_labels = []

    for image_path in DATASET_DIR.rglob("*"):
        if not image_path.is_file():
            continue

        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        # The immediate parent folder should be the disease.
        folder_name = image_path.parent.name.strip().lower()
        canonical_name = DISEASE_FOLDERS.get(folder_name)

        if canonical_name is None:
            print(
                f"Skipping image in unrecognized folder: "
                f"{image_path}"
            )
            continue

        image_paths.append(str(image_path))
        image_labels.append(CLASS_NAMES.index(canonical_name))

    if not image_paths:
        raise ValueError(
            "No usable images found. Check that dataset contains "
            "plant folders, each with Healthy, Leaf Spot, "
            "Powdery Mildew, and Rust subfolders."
        )

    return image_paths, image_labels


# --------------------------------------------------
# 4. SPLIT IMAGES INTO TRAINING AND VALIDATION SETS
# --------------------------------------------------

def split_dataset(paths, labels):
    grouped = {i: [] for i in range(len(CLASS_NAMES))}

    for path, label in zip(paths, labels):
        grouped[label].append(path)

    train_paths = []
    train_labels = []
    val_paths = []
    val_labels = []

    for label, class_paths in grouped.items():
        random.shuffle(class_paths)

        if len(class_paths) < 2:
            raise ValueError(
                f"Class '{CLASS_NAMES[label]}' has only "
                f"{len(class_paths)} image(s). At least 2 are "
                "needed for a training/validation split."
            )

        # Keep at least one image for validation and training.
        val_count = max(1, round(len(class_paths) * 0.2))
        val_count = min(val_count, len(class_paths) - 1)

        val_part = class_paths[:val_count]
        train_part = class_paths[val_count:]

        train_paths.extend(train_part)
        train_labels.extend([label] * len(train_part))

        val_paths.extend(val_part)
        val_labels.extend([label] * len(val_part))

        print(
            f"{CLASS_NAMES[label]}: "
            f"{len(train_part)} training, "
            f"{len(val_part)} validation"
        )

    return (
        train_paths,
        train_labels,
        val_paths,
        val_labels,
    )


# --------------------------------------------------
# 5. LOAD AND PREPARE IMAGES
# --------------------------------------------------

def load_images(paths):
    images = []

    for index, path in enumerate(paths, start=1):
        image = tf.keras.utils.load_img(
            path,
            target_size=IMAGE_SIZE,
            color_mode="rgb",
        )

        image_array = tf.keras.utils.img_to_array(image)
        images.append(image_array)

        if index % 50 == 0:
            print(f"Loaded {index}/{len(paths)} images")

    return np.asarray(images, dtype=np.float32)


# --------------------------------------------------
# 6. BUILD THE DISEASE CLASSIFICATION MODEL
# --------------------------------------------------

def build_model():
    # ImageNet pretrained weights require an internet
    # connection on the first run if not already cached.
    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3),
    )

    # First train the new classification layers only.
    base_model.trainable = False

    inputs = layers.Input(shape=(224, 224, 3))

    # Small random changes help reduce overfitting.
    x = layers.RandomFlip("horizontal")(inputs)
    x = layers.RandomRotation(0.05)(x)
    x = layers.RandomZoom(0.1)(x)

    x = layers.Lambda(preprocess_input)(x)

    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.2)(x)

    outputs = layers.Dense(
        len(CLASS_NAMES),
        activation="softmax",
    )(x)

    model = models.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


# --------------------------------------------------
# 7. TRAIN AND SAVE THE MODEL
# --------------------------------------------------

def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    print("\nScanning dataset...")
    paths, labels = collect_images()

    print(f"\nTotal usable images: {len(paths)}")

    print("\nImages found per class:")
    for index, name in enumerate(CLASS_NAMES):
        count = sum(1 for label in labels if label == index)
        print(f"{name}: {count}")

    train_paths, train_labels, val_paths, val_labels = (
        split_dataset(paths, labels)
    )

    print("\nLoading training images...")
    x_train = load_images(train_paths)
    y_train = np.asarray(train_labels, dtype=np.int32)

    print("\nLoading validation images...")
    x_val = load_images(val_paths)
    y_val = np.asarray(val_labels, dtype=np.int32)

    print("\nBuilding model...")
    model = build_model()
    model.summary()

    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=4,
            restore_best_weights=True,
        ),
        ModelCheckpoint(
            filepath=str(MODEL_PATH),
            monitor="val_loss",
            save_best_only=True,
        ),
    ]

    print("\nStarting training...")
    model.fit(
        x_train,
        y_train,
        validation_data=(x_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        shuffle=True,
        callbacks=callbacks,
        verbose=1,
    )

    # Save the final best-weight model.
    model.save(MODEL_PATH)

    with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as file:
        json.dump(CLASS_NAMES, file, indent=4)

    print("\nTraining completed!")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Class labels saved to: {CLASS_NAMES_PATH}")

    loss, accuracy = model.evaluate(
        x_val,
        y_val,
        verbose=0,
    )

    print(f"\nValidation loss: {loss:.4f}")
    print(f"Validation accuracy: {accuracy:.2%}")
    print(
        "\nImportant: validation accuracy is only an initial "
        "estimate, especially with a small dataset."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("\nTRAINING FAILED")
        print(f"{type(error).__name__}: {error}")
        traceback.print_exc()
