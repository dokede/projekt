from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Renderuje plik index.html

if __name__ == "__main__":
    # Importujemy `os`, aby pobrać numer portu z zmiennej środowiskowej
    import os
    
    # Pobieramy port z systemu, domyślnie ustawiamy na 5000 (na wypadek, gdyby zmienna nie była ustawiona)
    port = int(os.environ.get("PORT", 5000))
    
    # Uruchamiamy aplikację na podanym porcie
    app.run(host="0.0.0.0", port=port, debug=True)
