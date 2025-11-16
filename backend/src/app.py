import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import cv2
import uuid
import mysql.connector

db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
cursor = db.cursor(dictionary=True)


app = Flask(__name__)
CORS(app)

MODEL_PATH = "../checkpoints/test_model.keras"
UPLOAD_FOLDER = "uploads"
HEATMAP_FOLDER = "heatmaps"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HEATMAP_FOLDER, exist_ok=True)

model = tf.keras.models.load_model("../checkpoints/test_model.keras")


dummy = np.zeros((1, 64, 64, 3), dtype=np.float32)
_ = model(dummy, training=False)

def generate_gradcam(model, img_array, last_conv_layer_name="conv2d_2"):

    last_conv_layer = model.get_layer(last_conv_layer_name)

    conv_model = tf.keras.models.Model(
        inputs=model.layers[0].input,
        outputs=last_conv_layer.output         
    )

    classifier_input = tf.keras.Input(shape=last_conv_layer.output.shape[1:])
    x = classifier_input

    for layer in model.layers[model.layers.index(last_conv_layer)+1:]:
        x = layer(x)

    classifier_model = tf.keras.models.Model(classifier_input, x)

    with tf.GradientTape() as tape:
        conv_output = conv_model(img_array)
        tape.watch(conv_output)

        preds = classifier_model(conv_output)
        top_class = tf.argmax(preds[0])
        loss = preds[:, top_class]

    grads = tape.gradient(loss, conv_output)[0]
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1))

    conv_output = conv_output[0]

    heatmap = tf.zeros(conv_output.shape[:2], dtype=tf.float32)

    for i in range(pooled_grads.shape[0]):
        heatmap += pooled_grads[i] * conv_output[:, :, i]

    heatmap = tf.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap)

    return heatmap.numpy()


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["file"]
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        img = image.load_img(filepath, target_size=(64, 64))
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        preds = model.predict(img_array)

        predicted_class = int(np.argmax(preds[0]))
        confidence = float(np.max(preds[0]) * 100)

        labels = ["Non-Demented", "Very Mild Demented", "Mild Demented", "Moderate Demented"]
        predicted_label = labels[predicted_class]

        heatmap = generate_gradcam(model, img_array)

        heatmap = cv2.resize(heatmap, (64, 64))
        heatmap = np.uint8(255 * heatmap)

        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        original = cv2.imread(filepath)
        original = cv2.resize(original, (64, 64))

        superimposed_img = cv2.addWeighted(original, 0.6, heatmap, 0.4, 0)

        heatmap_filename = f"heatmap_{uuid.uuid4().hex}.jpg"
        heatmap_path = os.path.join(HEATMAP_FOLDER, heatmap_filename)
        cv2.imwrite(heatmap_path, superimposed_img)

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO predictions (user_id, prediction_label, prediction_confidence,
                                    original_image_path, heatmap_image_path, model_version)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            request.form.get("user_id"),
            predicted_label,
            confidence,  
            filepath,
            heatmap_path,
            "v1.0"
        ))

        db.commit()
        prediction_id = cursor.lastrowid
    
        cursor.execute("""
            INSERT INTO analysis_results (user_id, prediction, confidence)
            VALUES (%s, %s, %s)
        """, (
            request.form.get("user_id"),
            predicted_label,
            confidence,
        ))

        db.commit()

        return jsonify({
            "prediction_id": prediction_id,
            "prediction": predicted_label,
            "confidence": confidence,
            "image_path": filepath,
            "heatmap_path": heatmap_path
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/history/<int:user_id>", methods=["GET"])
def get_history(user_id):
    cursor.execute("""
        SELECT prediction, confidence, created_at
        FROM analysis_results
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    results = cursor.fetchall()

    formatted = [
        {
            "date": r["created_at"].strftime("%Y-%m-%d %H:%M"),
            "prediction": r["prediction"],
            "confidence": round(r["confidence"], 2)
        }
        for r in results
    ]
    return jsonify(formatted)


@app.get("/api/predictions/<int:prediction_id>")
def get_prediction_details(prediction_id):
    cursor.execute("""
        SELECT *
        FROM predictions
        WHERE id = %s
    """, (prediction_id,))
    pred = cursor.fetchone()

    if not pred:
        return jsonify({"error": "Prediction not found"}), 404

    return jsonify(pred)


from flask import send_from_directory

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('uploads', filename)

@app.route('/heatmaps/<path:filename>')
def serve_heatmaps(filename):
    return send_from_directory('heatmaps', filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
