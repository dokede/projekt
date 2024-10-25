from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import io
import base64
import tensorflow as tf

app = Flask(__name__)

# Ładowanie modelu TensorFlow
model_filename = 'model.h5'  # Upewnij się, że ścieżka do modelu jest poprawna
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

        prediction = loaded_model.predict(image_array)
        predicted_class = np.argmax(prediction)  # Znalezienie klasy o najwyższym prawdopodobieństwie
        confidence = np.max(prediction) * 100  # Pobranie pewności (prawdopodobieństwa) przewidywanej klasy

        return jsonify({
            'prediction': int(predicted_class),
            'confidence': float(confidence)  # Zwróć pewność przewidywania
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Zwróć błąd w formacie JSON

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
