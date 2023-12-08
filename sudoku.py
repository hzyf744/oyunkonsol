import tkinter as tk
from tkinter import messagebox
import random

class SudokuOyunu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Oyunu")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.oyun_tahtasi = tk.Frame(root)
        self.oyun_tahtasi.pack()

        # Sudoku tahtası oluştur ve göster
        self.sudoku_tahtasi = self.sudoku_tahtasi_olustur()
        self.oyuncu_skoru = 0  # Yeni özellik: Oyuncu skoru

        self.oyun_tahtasini_goster()

    def sudoku_tahtasi_olustur(self):
        sudoku_tahtasi = [[0]*9 for _ in range(9)]

        # Sudoku tahtasını rastgele doldur
        for _ in range(20):
            satir = random.randint(0, 8)
            sutun = random.randint(0, 8)
            deger = random.randint(1, 9)

            while not self.gecerli_tahmin(sudoku_tahtasi, satir, sutun, deger):
                satir = random.randint(0, 8)
                sutun = random.randint(0, 8)
                deger = random.randint(1, 9)

            sudoku_tahtasi[satir][sutun] = deger

        return sudoku_tahtasi

    def gecerli_tahmin(self, tahta, satir, sutun, deger):
        for i in range(9):
            if tahta[satir][i] == deger or tahta[i][sutun] == deger:
                return False

        bas_satir, bas_sutun = 3 * (satir // 3), 3 * (sutun // 3)
        for i in range(3):
            for j in range(3):
                if tahta[bas_satir + i][bas_sutun + j] == deger:
                    return False

        return True

    def oyun_tahtasini_goster(self):
        for i in range(9):
            for j in range(9):
                deger = self.sudoku_tahtasi[i][j]

                if deger != 0:
                    renk = "white"
                    if (i // 3 + j // 3) % 2 == 0:
                        renk = "#FFD700"  # Altın rengi

                    label = tk.Label(self.oyun_tahtasi, text=str(deger),
                                     font=("Helvetica", 16), width=4, height=2, relief="solid", bg=renk)
                    label.grid(row=i, column=j, padx=2, pady=2)
                else:
                    entry = tk.Entry(self.oyun_tahtasi, font=("Helvetica", 16), width=4, justify="center")
                    entry.grid(row=i, column=j, padx=2, pady=2)

        kontrol_butonu = tk.Button(self.oyun_tahtasi, text="Çözümü Kontrol Et", command=self.kontrol_et,
                                   font=("Helvetica", 12), bg="#4CAF50", fg="white")
        kontrol_butonu.grid(row=9, columnspan=9, pady=10)

    def kontrol_et(self):
        for i in range(9):
            for j in range(9):
                entry = self.oyun_tahtasi.grid_slaves(row=i, column=j)[0]
                if entry.get() != "":
                    try:
                        deger = int(entry.get())
                        if not self.gecerli_tahmin(self.sudoku_tahtasi, i, j, deger):
                            messagebox.showerror("Hata", "Çözüm Yanlış!")
                            return
                    except ValueError:
                        messagebox.showerror("Hata", "Geçersiz Değer!")
                        return

        messagebox.showinfo("Başarılı", "Çözüm Doğru!")
        self.oyuncu_skoru += 1  # Yeni özellik: Oyuncu skorunu artır
        self.sudoku_tahtasi = self.sudoku_tahtasi_olustur()  # Yeni özellik: Yeni bir oyun başlat
        self.oyun_tahtasini_goster()

        # Yeni özellik: Oyun sonu mesajı
        if self.oyuncu_skoru >= 3:
            messagebox.showinfo("Oyun Bitti", f"Tebrikler! {self.oyuncu_skoru} oyun kazandınız.")

if __name__ == "__main__":
    root = tk.Tk()
    oyun = SudokuOyunu(root)
    root.mainloop()
