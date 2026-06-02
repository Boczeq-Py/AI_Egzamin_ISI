import streamlit as st
import random
import google.generativeai as genai

# Ustawienia strony
st.set_page_config(page_title="Symulator Egzaminu", page_icon="🎓")

# Pasek boczny do wpisania klucza API
with st.sidebar:
    st.header("⚙️ Ustawienia")
    api_key = st.text_input("Podaj swój klucz API Gemini:", type="password")
    st.info("Klucz nie jest nigdzie zapisywany. Znika po zamknięciu aplikacji.")

def ocen_odpowiedz(klucz, pytanie, wzorzec, odpowiedz_uzytkownika):
    """Funkcja łącząca się z Gemini w celu oceny odpowiedzi"""
    try:
        genai.configure(api_key=klucz)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Jesteś surowym, ale sprawiedliwym wykładowcą akademickim z przedmiotu Inżynieria Systemów Informacyjnych.
        Twoim zadaniem jest ocenić odpowiedź studenta.

        Pytanie: {pytanie}
        Wzorcowa odpowiedź (to student powinien wiedzieć): {wzorzec}
        Odpowiedź studenta: {odpowiedz_uzytkownika}

        Zwróć ocenę w skali od 1 do 10 oraz krótki, bezpośredni feedback (co było dobrze, a czego zabrakło). 
        Formatuj odpowiedź dokładnie tak:
        **Ocena:** [Twoja ocena]/10
        **Feedback:** [Twój komentarz]
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Wystąpił błąd podczas łączenia z AI: {e}"

# Rozszerzona Baza Wiedzy (ponad 20 pytań!)
baza_wiedzy = {
    # --- TEMAT 1: SYSTEMY INFORMACYJNE ---
    "Czym różni się System Informacyjny od Systemu Informatycznego?":
        "System Informacyjny to szerokie pojęcie obejmujące ludzi, procesy biznesowe, dane, sieci, sprzęt i oprogramowanie. System informatyczny to narzędzie, które służy do automatyzacji systemu informacyjnego.",
    "Wymień 6 głównych składowych Systemu Informacyjnego.":
        "1. Sprzęt\n2. Oprogramowanie\n3. Dane\n4. Sieci\n5. Procedury\n6. Ludzie (najważniejszy element).",
    "Czym różnią się wymagania funkcjonalne od niefunkcjonalnych w projektowaniu systemów?":
        "Wymagania funkcjonalne określają to, CO system ma robić (np. 'system musi pozwalać na generowanie faktur'). Wymagania niefunkcjonalne określają to, JAK system ma działać (np. 'czas odpowiedzi poniżej 1 sekundy', 'wysoka skalowalność', 'bezpieczeństwo').",

    # --- TEMAT 2 & 3: ARCHITEKTURY I MVC ---
    "Opisz krótko architekturę 3-warstwową (3-Tier).":
        "Dzieli aplikację na trzy warstwy: 1. Prezentacji (UI), 2. Logiki biznesowej (Backend), 3. Danych (Baza danych).",
    "Czym charakteryzuje się architektura komponentowa i jakie są jej dwie złote zasady?":
        "Budowanie aplikacji z niezależnych modułów. Zasady: Wysoka spójność (High Cohesion - robi jedną rzecz) oraz Słabe powiązanie (Loose Coupling - komponenty nie wiedzą o sobie za wiele).",
    "Wyjaśnij różnicę między podejściem SSR (Server-Side Rendering) a SPA (Single Page Application).":
        "W SSR serwer generuje od razu gotowy kod HTML i wysyła do przeglądarki. W SPA frontend to osobna aplikacja, która pobiera z backendu tylko surowe dane w formacie JSON przez API REST.",
    "Opisz trzy filary wzorca projektowego MVC.":
        "1. Model (dane i logika), 2. View/Widok (warstwa prezentacji), 3. Controller/Kontroler (odbiera żądania i przekazuje do Modelu/Widoku).",
    "Do czego służy technologia szablonów (np. Thymeleaf) w architekturze MVC?":
        "Służy do implementacji warstwy Widoku (View). Pozwala na dynamiczne wstrzykiwanie danych z Modelu (otrzymanych przez Kontroler) do statycznego kodu HTML przed jego wysłaniem do przeglądarki.",

    # --- TEMAT 4: IoC & DI ---
    "Wyjaśnij pojęcie Inversion of Control (IoC).":
        "Odwrócenie sterowania ('Nie dzwoń do nas, my zadzwonimy do ciebie'). Framework zarządza cyklem życia obiektów, zdejmując to z barków programisty.",
    "Czym jest Dependency Injection (DI) i jakie ma zalety?":
        "Realizacja IoC. Obiekty dostają zależności z zewnątrz, zamiast same je tworzyć. Zalety to m.in. łatwiejsze testowanie i mniejsze powiązanie kodu.",
    "Wymień 3 sposoby wstrzykiwania zależności (DI) i wskaż najbardziej zalecany.":
        "1. Przez konstruktor (najbardziej zalecany - obiekt od razu dostaje to, czego potrzebuje). 2. Przez metodę ustawiającą (Setter). 3. Przez pole (np. @Autowired - obecnie uważane za antywzorzec).",

    # --- TEMAT 5: ORM ---
    "Wyjaśnij, czym jest ORM (Object-Relational Mapping).":
        "Technika mapowania obiektów w kodzie na tabele w relacyjnej bazie danych. Chroni przed SQL Injection i ułatwia tworzenie zapytań bez pisania surowego SQL.",
    "Na czym polega problem N+1 zapytań w ORM?":
        "Problem wydajnościowy. Pobieranie głównej listy to 1 zapytanie, a potem dla każdego elementu z N wysyłane jest osobne zapytanie o szczegóły (łącznie N+1 zapytań do bazy zamiast jednego zoptymalizowanego).",

    # --- TEMAT 6: WEB SERVICES ---
    "Porównaj krótko architekturę REST i SOAP.":
        "REST to lekki styl architektoniczny oparty na JSON i HTTP. SOAP to formalny protokół oparty na XML i ścisłym kontrakcie (WSDL), często używany w bankowości ze względu na wbudowane mechanizmy bezpieczeństwa.",

    # --- TEMAT 7, 8, 9: BEZPIECZEŃSTWO I AUTORYZACJA ---
    "Jaka jest rola filtrów w aplikacjach webowych? Podaj przykłady.":
        "Filtry przechwytują żądania HTTP zanim trafią one do logiki aplikacji. Przykłady: sprawdzanie uprawnień (autoryzacja), blokowanie złośliwego ruchu, logowanie statystyk (audyt).",
    "Jaka jest różnica między uwierzytelnianiem a autoryzacją?":
        "Uwierzytelnianie to sprawdzenie tożsamości ('Kim jesteś?', np. login/hasło). Autoryzacja to sprawdzenie uprawnień ('Co wolno ci zrobić?').",
    "Porównaj Sesję HTTP z Tokenami JWT.":
        "Sesja HTTP zapisuje stan na serwerze (stateful). JWT to zaszyfrowany token trzymany przez klienta (stateless, idealne do skalowalnych mikroserwisów).",
    "Czym jest OAuth 2.0 i jakie role w nim występują?":
        "Standard delegowania uprawnień. Role: Właściciel zasobu, Klient (aplikacja trzecia), Serwer Autoryzacyjny (wydaje tokeny), Serwer Zasobów (trzyma dane).",

    # --- TEMAT 10 & 11: MIKROSERWISY I KOLEJKI ---
    "Podaj główne założenia architektoniczne mikroserwisów.":
        "Małe, niezależne usługi, własna baza danych dla każdego serwisu (brak współdzielenia tabel), komunikacja przez API lub kolejki, możliwość użycia różnych technologii.",
    "Wymień główne wady i wyzwania związane z zastosowaniem architektury mikroserwisów.":
        "Trudniejsze wdrożenia i skomplikowana infrastruktura, trudniejsze debugowanie błędów wędrujących między serwisami oraz opóźnienia i problemy z siecią.",
    "Jak działa asynchroniczna kolejka komunikatów?":
        "Pozwala na pracę w tle (nadawca nie czeka na odpowiedź). Składa się z Producenta (wysyła), Brokera (przechowuje, np. RabbitMQ) i Konsumenta (odbiera).",

    # --- TEMAT 12: TESTOWANIE ---
    "Opisz różnicę między testami jednostkowymi a integracyjnymi.":
        "Jednostkowe testują mały fragment w izolacji (z mockami/atrapami bazy danych). Integracyjne sprawdzają współpracę wielu modułów, często łącząc się z prawdziwą bazą, przez co są wolniejsze.",
    "Na czym polega różnica między metodykami TDD a BDD?":
        "TDD (Test-Driven Development) to pisanie najpierw testu, a potem kodu (Red-Green-Refactor). BDD (Behavior-Driven Development) skupia się na testowaniu zachowań biznesowych, a testy pisane są językiem zrozumiałym dla klienta (schemat Given-When-Then)."
}

# Zarządzanie stanem - Inicjalizacja
if 'aktualne_pytanie' not in st.session_state:
    st.session_state.aktualne_pytanie = random.choice(list(baza_wiedzy.keys()))

if 'sprawdzono' not in st.session_state:
    st.session_state.sprawdzono = False

st.title("🎓 Symulator Egzaminu")
st.subheader("Inżynieria Systemów Informacyjnych")

# Panel do losowania
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Wylosuj inne"):
        st.session_state.aktualne_pytanie = random.choice(list(baza_wiedzy.keys()))
        st.rerun()

st.info(f"**Pytanie dla Ciebie:**\n\n{st.session_state.aktualne_pytanie}")

# Pole odpowiedzi
st.text_area("Twoja odpowiedź:", height=150, placeholder="Zacznij pisać tutaj...", key="user_input")

# Tryb pisania
if not st.session_state.sprawdzono:
    if st.button("Sprawdź z AI"):
        if st.session_state.user_input.strip():
            st.session_state.sprawdzono = True
            st.rerun()
        else:
            st.warning("Najpierw wpisz odpowiedź!")

# Tryb sprawdzania
if st.session_state.sprawdzono:
    if not api_key:
        st.error("Wklej swój klucz API Gemini w lewym panelu, aby otrzymać ocenę!")
        if st.button("Wróć i podaj klucz"):
            st.session_state.sprawdzono = False
            st.rerun()
    else:
        st.markdown("### Twoja odpowiedź:")
        st.write(st.session_state.user_input)

        with st.spinner("AI analizuje Twoją odpowiedź..."):
            wynik_ai = ocen_odpowiedz(
                klucz=api_key,
                pytanie=st.session_state.aktualne_pytanie,
                wzorzec=baza_wiedzy[st.session_state.aktualne_pytanie],
                odpowiedz_uzytkownika=st.session_state.user_input
            )

        st.markdown("---")
        st.subheader("🤖 Werdykt Egzaminatora")

        if "Ocena:" in wynik_ai:
            try:
                ocena_str = wynik_ai.split("Ocena:")[1].split("/10")[0].replace("**", "").strip()
                ocena = int(ocena_str)

                if ocena >= 8:
                    st.success(wynik_ai)
                    st.balloons()
                elif ocena >= 5:
                    st.warning(wynik_ai)
                else:
                    st.error(wynik_ai)
            except:
                st.info(wynik_ai)
        else:
            st.info(wynik_ai)

        with st.expander("Pokaż oryginalną notatkę wzorcową"):
            st.write(baza_wiedzy[st.session_state.aktualne_pytanie])

        if st.button("Kolejne pytanie"):
            st.session_state.sprawdzono = False
            st.session_state.user_input = ""
            st.session_state.aktualne_pytanie = random.choice(list(baza_wiedzy.keys()))
            st.rerun()