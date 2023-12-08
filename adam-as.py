import streamlit as st
import random

def kelime_sec():
    kelimeler = [
        "python", "gelişim", "programlama", "oyun", "veri", "yapayzeka", "kodlama",
        "öğrenme", "bilgisayar", "proje", "developer", "framework", "teknoloji",
        "program", "kütüphane", "backend", "frontend", "web", "mobil",
        "algoritma", "veritabanı", "grafik", "insan", "doğa", "gezegen",
        "evren", "gezegen", "evrim", "döngü", "özellik", "fonksiyon",
        "sistem", "platform", "çerçeve", "görselleştirme", "kodlayıcı", "entegrasyon",
        "mimari", "etkileşim", "güvenlik", "ağ", "siber", "bağlantı"
        # Toplam 50 kelime ekleyerek listeyi doldurabilirsiniz.
    ]
    return random.choice(kelimeler)

def kelime_ekle():
    yeni_kelime = st.text_input("Eklemek istediğiniz yeni kelimeyi girin:")
    return yeni_kelime.lower()

def kelime_guncelle(kelimeler):
    st.subheader("Mevcut Kelimeler:")
    for kelime in kelimeler:
        st.text("- " + kelime)
    return kelime_ekle()

def harf_tahmin_et(kelime, dogru_harfler):
    kelime_gosterimi = ""
    for harf in kelime:
        if harf.lower() in dogru_harfler:
            kelime_gosterimi += harf + " "
        else:
            kelime_gosterimi += "_ "
    return kelime_gosterimi.strip()

def adam_asmaca(cizim):
    asma_seviyeleri = [
        """
        -----
        |   |
        |
        |
        |
        |
        -
        """,
        """
        -----
        |   |
        |   O
        |
        |
        |
        -
        """,
        """
        -----
        |   |
        |   O
        |   |
        |
        |
        -
        """,
        """
        -----
        |   |
        |   O
        |  /|
        |
        |
        -
        """,
        """
        -----
        |   |
        |   O
        |  /|\\
        |
        |
        -
        """,
        """
        -----
        |   |
        |   O
        |  /|\\
        |  /
        |
        -
        """,
        """
        -----
        |   |
        |   O
        |  /|\\
        |  / \\
        |
        -
        """
    ]
    return asma_seviyeleri[cizim]

def oyun_durumu_goster(kelime, dogru_harfler, yanlis_harfler, can):
    st.subheader("Oyun Durumu:")
    st.text("Kelime: " + harf_tahmin_et(kelime, dogru_harfler))
    st.text("Doğru Harfler: " + ", ".join(sorted(dogru_harfler)))
    st.text("Yanlış Harfler: " + ", ".join(sorted(yanlis_harfler)))
    st.text(adam_asmaca(6 - can))
    st.text(f"Kalan Can: {can}\n")

def kelime_istegi():
    return st.text_input("Oyunu özelleştirin! Bir kelime ekleyin veya rastgele bir kelime isteyin:")

def oyun_bitti_mi(can, dogru_harfler, kelime):
    return can == 0 or set(kelime.lower()) == dogru_harfler

def oyun_sonu_menusu():
    while True:
        secim = st.text_input("Yeniden başlatmak için 'Y', çıkmak için 'Ç' girin:").lower()
        if secim == "y":
            return True
        elif secim == "ç":
            return False
        else:
            st.warning("Geçersiz giriş. Lütfen 'Y' veya 'Ç' girin.")

def adam_asmaca_oyunu():
    st.title("Adam Asmaca Oyunu")

    while True:
        kelime = kelime_istegi() if st.checkbox("Oyunu özelleştirmek ister misiniz?") else kelime_sec()
        
        dogru_harfler = set()
        yanlis_harfler = set()
        can = 6

        while True:
            oyun_durumu_goster(kelime, dogru_harfler, yanlis_harfler, can)
            harf = st.text_input("Bir harf tahmin edin:").lower()

            if harf.isalpha() and len(harf) == 1:
                if harf in kelime.lower():
                    dogru_harfler.add(harf)
                else:
                    yanlis_harfler.add(harf)
                    can -= 1

                if oyun_bitti_mi(can, dogru_harfler, kelime):
                    break
            else:
                st.warning("Geçersiz giriş. Lütfen bir harf girin.")

        oyun_durumu_goster(kelime, dogru_harfler, yanlis_harfler, can)

        if can == 0:
            st.error(f"Üzgünüm! Kelimeyi bulamadınız. Doğru kelime: {kelime}")
        else:
            st.success(f"Tebrikler! Kelimeyi buldunuz. Kelime: {kelime}")

        if not oyun_sonu_menusu():
            break

if __name__ == "__main__":
    adam_asmaca_oyunu()
