from model_transfer import create_transfer_model
from data_preprocessing import create_data_generators
from config import *

from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from model_transfer import create_transfer_model
from data_preprocessing import create_data_generators
from config import *

from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

train_gen, val_gen = create_data_generators(TRAIN_DIR, img_size=(224,224), batch_size=BATCH_SIZE)

model = create_transfer_model(input_shape=(224,224,3), num_classes=4)

checkpoint = ModelCheckpoint("../checkpoints/transfer_model.keras", save_best_only=True, monitor='val_accuracy')
early_stop = EarlyStopping(patience=5, restore_best_weights=True)
lr_reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=3)

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=[checkpoint, early_stop, lr_reduce]
)

train_gen, val_gen = create_data_generators(TRAIN_DIR, img_size=(224,224), batch_size=BATCH_SIZE)

model = create_transfer_model(input_shape=(None, 225,224,3), num_classes=4)

checkpoint = ModelCheckpoint("../checkpoints/transfer_model.keras", save_best_only=True, monitor='val_accuracy')
early_stop = EarlyStopping(patience=5, restore_best_weights=True)
lr_reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=3)

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=[checkpoint, early_stop, lr_reduce]
)
