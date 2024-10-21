const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
let drawing = false;

// Ustawienia rysowania
context.lineWidth = 15; // Grubość linii
context.lineCap = 'round'; // Umożliwia zaokrąglone końce linii
context.strokeStyle = 'black'; // Kolor linii

// Ustawienie tła na białe na początku
context.fillStyle = 'white';
context.fillRect(0, 0, canvas.width, canvas.height);

// Rozpoczęcie rysowania
canvas.addEventListener('mousedown', (event) => {
    drawing = true;
    context.beginPath(); // Rozpocznij nową ścieżkę
    const rect = canvas.getBoundingClientRect();
    context.moveTo(event.clientX - rect.left, event.clientY - rect.top);
});

// Kończenie rysowania
canvas.addEventListener('mouseup', () => {
    drawing = false;
});

// Rysowanie na płótnie
canvas.addEventListener('mousemove', (event) => {
    if (!drawing) return;

    const rect = canvas.getBoundingClientRect();
    context.lineTo(event.clientX - rect.left, event.clientY - rect.top);
    context.stroke(); // Rysuj linię
});

// Zapisz obrazek po kliknięciu przycisku
document.getElementById('save').addEventListener('click', () => {
    const dataURL = canvas.toDataURL('image/png');

    fetch('/save_image', {
        method: 'POST',
        body: JSON.stringify({ image: dataURL }),
        headers: { 'Content-Type': 'application/json' }
    }).then(response => {
        return response.json(); // Odbierz odpowiedź jako JSON
    }).then(data => {
        document.getElementById('result').innerText = 
            `Przewidywana cyfra: ${data.predicted_class}, Pewność: ${data.confidence}%`; // Wyświetl wynik
    }).catch(error => {
        console.error('Błąd podczas zapisywania obrazu:', error);
    });
});

// Dodaj funkcjonalność czyszczenia płótna
document.getElementById('clear').addEventListener('click', () => {
    context.fillStyle = 'white';
    context.fillRect(0, 0, canvas.width, canvas.height); // Wypełnij białym kolorem
    document.getElementById('result').innerText = ''; // Wyczyść wynik
});

// Ustawienie tła na białe przy załadowaniu strony
window.onload = function() {
    context.fillStyle = 'white';
    context.fillRect(0, 0, canvas.width, canvas.height);
};

