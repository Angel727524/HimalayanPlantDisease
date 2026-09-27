import tensorflow as tf
from tensorflow.keras import layers, models
from pathlib import Path

# =========================
# SETTINGS
# =========================

DATASET_DIR = Path("dataset")

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 4
EPOCHS = 5

# =========================
# LOAD DATASET
# =========================

print("Loading dataset...")

dataset = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True
)

class_names = dataset.class_names
num_classes = len(class_names)

print("\nPlant classes:")
for i, name in enumerate(class_names):
    print(i, "-", name)

print("\nNumber of classes:", num_classes)

# =========================
# PREPARE DATA
# =========================

dataset_size = tf.data.experimental.cardinality(dataset).numpy()

if dataset_size < 2:
    print("\nNot enough data to create training and validation sets.")
    print("We will test the model structure only.")
    train_dataset = dataset
    validation_dataset = dataset
else:
    validation_size = max(1, int(dataset_size * 0.2))

    validation_dataset = dataset.take(validation_size)
    train_dataset = dataset.skip(validation_size)

# =========================
# DATA AUGMENTATION
# =========================

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# =========================
# MOBILE NET V2
# =========================

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

# =========================
# BUILD MODEL
# =========================

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),

    data_augmentation,

    layers.Rescaling(
        1.0 / 127.5,
        offset=-1
    ),

    base_model,

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.2),

    layers.Dense(
        num_classes,
        activation="softmax"
    )
])

# =========================
# COMPILE
# =========================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =========================
# TRAIN
# =========================

print("\nStarting training...")

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS
)

# =========================
# SAVE MODEL
# =========================

Path("models").mkdir(exist_ok=True)

model.save("models/plant_model.keras")

print("\nModel saved successfully!")
print("Location: models/plant_model.keras")