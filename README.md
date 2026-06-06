# AI-Egzaminator 🎓

Prosta aplikacja w Pythonie (Streamlit) do nauki na egzamin z Inżynierii Systemów Informacyjnych. Aplikacja losuje pytania z bazy, a model AI (Google Gemini) ocenia Twoje odpowiedzi tekstowe w skali 1-10 i daje krótki feedback.

## Wymagania

* Python 3.8+
* Klucz API do Google Gemini (darmowy)

## Jak zdobyć klucz API?

1. Wejdź na stronę [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Zaloguj się kontem Google.
3. Kliknij **"Create API key"** i skopiuj wygenerowany klucz. Wkleisz go bezpośrednio w aplikacji.

## Instalacja i uruchomienie

Pobierz kod i otwórz terminal w folderze z projektem.

1. Zainstaluj wymagane biblioteki z pliku konfiguracyjnego:
```
pip install -r requirements.txt
```
Uruchom aplikację:
```
python -m streamlit run App.py
```
