import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Konfiguracja strony
st.set_page_config(page_title="ProstyPlon", layout="centered")

st.title("🌱 ProstyPlon")
st.subheader("Szybki generator ofert")

# Nasza prosta baza produktów (łatwo tu dopisać nowe!)
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

# 2. Moduł zdjęciowy (na telefonie automatycznie zaproponuje aparat)
zdjecie_plik = st.file_uploader("Dodaj zdjęcie z galerii lub zrób nowe", type=["jpg", "jpeg", "png"])

if zdjecie_plik is not None:
    # Pobieramy zdjęcie
    img = Image.open(zdjecie_plik)
    
    # Skalujemy do rozsądnej szerokości, żeby zachować proporcje i czytelność tekstu na chmurze
    bazowa_szerokosc = 800
    proporcja = (bazowa_szerokosc / float(img.size[0]))
    nowa_wysokosc = int((float(img.size[1]) * float(proporcja)))
    img = img.resize((bazowa_szerokosc, nowa_wysokosc), Image.Resampling.LANCZOS)
    
    # Rysujemy półprzezroczysty pasek z ceną na dole zdjęcia
    draw = ImageDraw.Draw(img, "RGBA")
    szerokosc, wysokosc = img.size
    wysokosc_paska = int(wysokosc * 0.15)
    
    # Tło paska (czarne, półprzezroczyste)
    draw.rectangle(
        [(0, wysokosc - wysokosc_paska), (szerokosc, wysokosc)],
        fill=(0, 0, 0, 160)
    )
    
    # Tekst oferty (w MVP używamy domyślnej czcionki, ale ją powiększamy optycznie przez format)
    tekst = f"{produkt} | Waga: {waga} kg | CENA: {cena_koncowa:.2f} zl\nOdbior: {lokalizacja}"
    
    # UWAGA: Aby dodać piękny duży font, w pełnej wersji dorzucimy plik np. Arial.ttf.
    # W MVP zostawiamy czysty kod.
    draw.text((20, wysokosc - wysokosc_paska + 15), tekst, fill="white")
    
    # 3. Pokazujemy wynik
    st.image(img, caption="Podgląd Twojej oferty", use_container_width=True)
    
    # 4. Przycisk do pobrania
    buf = io.BytesIO()
    img.convert('RGB').save(buf, format="JPEG", quality=90)
    byte_im = buf.getvalue()
    
    st.download_button(
        label="📸 Pobierz gotowe zdjęcie do wrzucenia na grupę",
        data=byte_im,
        file_name="prostyplon_oferta.jpg",
        mime="image/jpeg"
    )
