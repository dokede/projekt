import json
from rapidfuzz import process

# Baza wiedzy (możesz ją załadować z pliku JSON)
portfolio_info = {
    "doświadczenie": "Pracuję w analizię mam od początku 2023 roku",
    "projekty": "Projekty wypisane są powyżej",
    "technologie": "Używam głównie pythona, sql, excel",
    "umiejętności": "Używam głównie pythona, sql, excel",
    "kontakt": "Skontaktuj się ze mną poprzez email: dominik2068@o2.pl.",
    "wykształcenie": "Jestem absolwentem Uniwersytetu Łódzkiego na kierunku Analiza Danych."
}

def chatbot_response(user_input):
    # Zamiana na małe litery (ułatwia porównanie)
    user_input = user_input.lower()
    
    # Dopasowanie z użyciem RapidFuzz
    best_match = process.extractOne(user_input, portfolio_info.keys())
    
    if best_match is not None and best_match[1] > 70:  # Próg podobieństwa, jeśli dopasowanie jest wystarczająco wysokie
        return portfolio_info[best_match[0]]  # Zwróć odpowiednią wartość na podstawie dopasowanej kategorii
    else:
        return "Nie jestem pewien, co masz na myśli. Spróbuj zapytać inaczej."

# Przykładowe zapytania:
print(chatbot_response("Jakie masz doświadczenie?"))
print(chatbot_response("Co umiesz zrobić?"))
print(chatbot_response("Jaki masz kontakt?"))
