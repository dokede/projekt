from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
import base64
from PIL import Image
import io

app = Flask(__name__)

# Wczytaj model
model = load_model('cnn_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.get_json()
    image_data = data['image']

    # Oczyszczenie danych obrazu
    image_data = image_data.split(',')[1]  # Pomijamy początkowy nagłówek
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))

    # Zmieniamy kolory (czarne tło, biała kreska)
    image = image.convert("L")  # Konwertuj na odcienie szarości
    image = Image.eval(image, lambda x: 255 - x)  # Inwersja kolorów

    # Zmiana rozmiaru do 28x28
    image = image.resize((28, 28))

    # Przetwórz obrazek do formatu odpowiedniego dla modelu
    img_array = np.array(image)
    img_array = img_array.reshape(1, 28, 28, 1).astype('float32') / 255

    # Przewidywanie
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction) * 100  # Pewność w procentach

    return jsonify({
        'predicted_class': int(predicted_class),
        'confidence': round(confidence, 2)  # Round to 2 decimal places
    })

if __name__ == '__main__':
    app.run(debug=True)
