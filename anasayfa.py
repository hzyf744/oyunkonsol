import streamlit as st
import subprocess

def main():
    st.title("Oyun Anasayfa")

    # Sudoku Oyunu
    st.header("Sudoku Oyunu")
    if st.button("Sudoku Oyununu Başlat"):
        run_game("sudoku.py")

    # Masa Tenisi Oyunu
    st.header("Masa Tenisi Oyunu")
    if st.button("Masa Tenisi Oyununu Başlat"):
        run_game("masa-tenisi.py")

    # Adam Asmaca Oyunu
    st.header("Adam Asmaca Oyunu")
    if st.button("Adam Asmaca Oyununu Başlat"):
        run_game("adam-as.py")

def run_game(file_name):
    command = f"streamlit run {file_name}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Çıktıları okuma ve ekrana yazdırma
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    # Process tamamlandığında çıktıları okuma
    rc = process.poll()
    print(f"Return code: {rc}")

if __name__ == "__main__":
    main()

