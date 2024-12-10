from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import io
import base64
import tensorflow as tf
from chatbot import chatbot_response

app = Flask(__name__)

# Ładowanie modelu TensorFlow
model_filename = 'mnist_cnn_model.h5'
loaded_model = tf.keras.models.load_model(model_filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        image_data = data['image']

        # Oczyszczenie danych obrazu (base64 -> obrazek)
        image_data = image_data.split(',')[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        # Konwertowanie obrazu do odcieni szarości
        image = image.convert("L")
        # Zmiana rozmiaru obrazu na 28x28
        image = image.resize((28, 28), Image.LANCZOS)

        # Przekształcenie obrazu w tablicę NumPy
        image_array = np.array(image)

        # Rozszerzenie wymiarów, aby uzyskać kształt (1, 28, 28, 1)
        image_array = image_array.reshape(1, 28, 28, 1)

        # Normalizacja danych
        image_array = image_array.astype(np.float32) / 255.0

        # Predykcja za pomocą modelu TensorFlow
        prediction = loaded_model.predict(image_array)
        predicted_class = np.argmax(prediction)
        confidence = int(np.max(prediction) * 100)

        return jsonify({
            'prediction': int(predicted_class),
            'confidence': float(confidence)  # Zwróć pewność przewidywania
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Zwróć błąd w formacie JSON

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    bot_response = chatbot_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
