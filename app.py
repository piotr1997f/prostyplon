import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request
import os

# Konfiguracja strony
st.set_page_config(page_title="ProstyPlon", layout="centered")

st.title("🌱 ProstyPlon")
st.subheader("Szybki generator ofert")

# Pobieranie ładnej czcionki (automatycznie)
font_url = "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Medium.ttf"
font_path = "Roboto-Medium.ttf"
if not os.path.exists(font_path):
    try:
        urllib.request.urlretrieve(font_url, font_path)
    except Exception as e:
        pass # Jeśli zablokują, aplikacja i tak zadziała na domyślnej

# Nasza prosta baza produktów
produkty = {
    "Dynia na lampion (duża)": 3.00,
    "Dynia Hokkaido": 4.00,
    "Jabłka (prosto z sadu)": 3.50,
    "Gruszki (słodkie)": 5.00
}

# 1. Wybór produktu i wagi
produkt = st.selectbox("Co dzisiaj sprzedajemy?", list(produkty.keys()))
cena_za_kg = produkty[produkt]

col1, col2 = st.columns(2)
with col1:
    waga = st.number_input("Waga (kg):", min_value=0.1, value=1.0, step=0.1)
with col2:
    lokalizacja = st.text_input("Odbiór:", value="Skierniewice")

# Obliczenie ceny
cena_koncowa = waga * cena_za_kg
st.markdown(f"### Do zapłaty: **{cena_koncowa:.2f} zł**")

# 2. Moduł zdjęciowy 
zdjecie_plik = st.file_uploader("📸 Dodaj zdjęcie z galerii lub zrób nowe", type=["jpg", "jpeg", "png"])

if zdjecie_plik is not None:
    # Pobieramy zdjęcie
    img = Image.open(zdjecie_plik)
    
    # Skalujemy do rozsądnej szerokości, żeby zachować proporcje
    bazowa_szerokosc = 800
    proporcja = (bazowa_szerokosc / float(img.size[0]))
    nowa_wysokosc = int((float(img.size[1]) * float(proporcja)))
    img = img.resize((bazowa_szerokosc, nowa_wysokosc), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(img, "RGBA")
    szerokosc, wysokosc = img.size
    
    # Próba załadowania pobranej czcionki, jeśli zawiedzie - domyślna
    try:
        font_duza = ImageFont.truetype(font_path, 42)
        font_mala = ImageFont.truetype(font_path, 30)
    except IOError:
        font_duza = ImageFont.load_default()
        font_mala = ImageFont.load_default()
    
    # Obliczanie wysokości paska na sztywno, żeby zmieścił dwie linie tekstu
    wysokosc_paska = 150
    
    # Tło paska (czarne, trochę ciemniejsze dla lepszego kontrastu)
    draw.rectangle(
        [(0, wysokosc - wysokosc_paska), (szerokosc, wysokosc)],
        fill=(0, 0, 0, 190)
    )
    
    # Przygotowanie tekstów
    linia1 = f"{produkt} ({waga} kg)"
    linia2 = f"CENA: {cena_koncowa:.2f} zł  |  Odbiór: {lokalizacja}"
    
    # Rysowanie tekstu z marginesami
    draw.text((30, wysokosc - wysokosc_paska + 20), linia1, fill="white", font=font_duza)
    draw.text((30, wysokosc - wysokosc_paska + 85), linia2, fill="#FFA500", font=font_mala) # Pomarańczowa cena
    
    # 3. Pokazujemy wynik
    st.image(img, caption="Podgląd Twojej oferty", use_container_width=True)
    
    # 4. Przycisk do pobrania
    buf = io.BytesIO()
    img.convert('RGB').save(buf, format="JPEG", quality=90)
    byte_im = buf.getvalue()
    
    st.download_button(
        label="📥 Pobierz gotowe zdjęcie z ofertą",
        data=byte_im,
        file_name="prostyplon_oferta.jpg",
        mime="image/jpeg"
    )
