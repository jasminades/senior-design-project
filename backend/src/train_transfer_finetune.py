import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"

import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from data_preprocessing import create_data_generators
from config import TRAIN_DIR, VAL_DIR, BATCH_SIZE, EPOCHS
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from visualize import plot_training_history

train_gen, val_gen = create_data_generators(TRAIN_DIR, img_size=(224,224), batch_size=BATCH_SIZE)

def create_transfer_model_finetune(input_shape=(224,224,3), num_classes=4, trainable_layers=30):
    base = MobileNetV2(
        include_top=False,
        input_shape=input_shape,
        weights="imagenet"
    )
    base.trainable = True
    for layer in base.layers[:-trainable_layers]:
        layer.trainable = False

    x = base.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.3)(x)
    out = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base.input, outputs=out)
    model.compile(
        optimizer=Adam(1e-5),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

checkpoint = ModelCheckpoint("../checkpoints/transfer_model_finetune.keras", 
                             save_best_only=True, monitor='val_accuracy')
early_stop = EarlyStopping(patience=5, restore_best_weights=True)
lr_reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=3)

model = create_transfer_model_finetune(input_shape=(224,224,3), num_classes=4, trainable_layers=0)
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=5,
    callbacks=[checkpoint, early_stop, lr_reduce]
)

val_gen.reset()
preds = model.predict(val_gen, verbose=1)
y_pred = np.argmax(preds, axis=1)
y_true = val_gen.classes

print("classification report:")
print(classification_report(y_true, y_pred, target_names=list(val_gen.class_indices.keys())))
print("confusion matrix:")
print(confusion_matrix(y_true, y_pred))

plot_training_history(history, title="Feature Extraction Phase")
plot_training_history(history, title="Fine-Tuning Phase")
