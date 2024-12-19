import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import numpy as np

# Załaduj zbiór danych MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Znormalizuj dane (0-255 -> 0-1) i dodaj dodatkowy wymiar dla kanału
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255

# Zamień etykiety na one-hot encoding
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Funkcja do tworzenia pojedynczego modelu CNN
def create_cnn(kernel_size):
    model = models.Sequential()
    model.add(layers.Conv2D(32, kernel_size=kernel_size, activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))  # Pierwszy pooling
    model.add(layers.Conv2D(64, kernel_size=kernel_size, activation='relu'))

    # Zmniejszamy liczbę poolingów i/lub zmniejszamy rozmiar filtra w trzeciej warstwie
    model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='relu'))  # Używamy mniejszego filtra

    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    return model

# Wybieramy rozmiar jądra (możesz zmienić to na (3, 3), (5, 5) lub (7, 7))
kernel_size = (5, 5)  # Przykład: Kernel 5x5
cnn = create_cnn(kernel_size)

# Kompilacja modelu
cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Trenujemy model
cnn.fit(x_train, y_train, epochs=2, batch_size=64, validation_data=(x_test, y_test))

# Dokonujemy prognoz
preds = cnn.predict(x_test)

# Ostateczna predykcja to klasa z największą wartością
preds_labels = np.argmax(preds, axis=1)
y_test_labels = np.argmax(y_test, axis=1)

# Oblicz dokładność modelu
accuracy = np.mean(preds_labels == y_test_labels)
print(f'Model Accuracy: {accuracy:.4f}')

# Zapisz model do pliku .h5
cnn.save('cnn_model.h5')

print("Model saved successfully!")
