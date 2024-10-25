from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import io
import base64
import tensorflow as tf  # Używamy TensorFlow do ładowania modelu

app = Flask(__name__)

# Ładowanie modelu TensorFlow
model_filename = '/home/dokede/mysite/model.h5'  # Upewnij się, że ścieżka do modelu jest poprawna
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
        image = image.resize((28, 28), Image.ANTIALIAS)

        # Przekształcenie obrazu w tablicę NumPy
        image_array = np.array(image)

        # Spłaszczenie tablicy do jednego wymiaru (784 cechy)
        image_array = image_array.flatten().reshape(1, 28 * 28)  # Zmieniamy kształt do (1, 784)

        # Normalizacja danych
        image_array = image_array.astype(np.float32) / 255.0

        # Predykcja za pomocą modelu TensorFlow
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
    # Importujemy `os`, aby pobrać numer portu z zmiennej środowiskowej
    import os
    
    # Pobieramy port z systemu, domyślnie ustawiamy na 5000 (na wypadek, gdyby zmienna nie była ustawiona)
    port = int(os.environ.get("PORT", 5000))
    
    # Uruchamiamy aplikację na podanym porcie
    app.run(host="0.0.0.0", port=port, debug=True)
