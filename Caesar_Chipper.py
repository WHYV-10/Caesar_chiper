import string
import tkinter as tk
from tkinter import messagebox

# ====== TEMA: BIRU ROYAL ======
WARNA, GELAP, MUDA, BG, BORDER = "#2563EB", "#1D4ED8", "#DBEAFE", "#EFF6FF", "#BFD3FF"
FONT = "Segoe UI"


def caesar(text, key, decrypt=False):
    if decrypt:
        key = -key
    hasil = ""
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            hasil += chr((ord(ch) - base + key) % 26 + base)
        else:
            hasil += ch
    return hasil


def tombol(parent, teks, cmd, bg, fg, hover):
    b = tk.Label(parent, text=teks, bg=bg, fg=fg, font=(FONT, 10, "bold"),
                 padx=20, pady=8, cursor="hand2")
    b.bind("<Button-1>", lambda e: cmd())
    b.bind("<Enter>", lambda e: b.config(bg=hover))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def kotak_teks(parent, tinggi):
    return tk.Text(parent, height=tinggi, width=54, font=("Consolas", 11), wrap="word",
                   relief="flat", bg="#F8FAFF", padx=8, pady=8,
                   highlightthickness=2, highlightbackground=BORDER, highlightcolor=WARNA)


def label(parent, teks):
    return tk.Label(parent, text=teks, bg="white", fg=GELAP, font=(FONT, 10, "bold"))


def update_preview(event=None):
    try:
        k = int(entry_key.get()) % 26
    except ValueError:
        preview.config(text="Masukkan kunci berupa angka")
        return
    abc = string.ascii_uppercase
    preview.config(text="Asli : " + " ".join(abc) + "\nGeser: " + " ".join(abc[k:] + abc[:k]))


def proses(decrypt):
    try:
        key = int(entry_key.get())
    except ValueError:
        messagebox.showerror("Error", "Kunci harus berupa angka!")
        return
    teks = input_text.get("1.0", tk.END).strip()
    if not teks:
        messagebox.showwarning("Peringatan", "Teks masih kosong!")
        return
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, caesar(teks, key, decrypt))
    status.config(text="Dekripsi berhasil" if decrypt else "Enkripsi berhasil")


def salin():
    hasil = output_text.get("1.0", tk.END).strip()
    if hasil:
        root.clipboard_clear()
        root.clipboard_append(hasil)
        status.config(text="Hasil disalin ke clipboard")


root = tk.Tk()
root.title("Caesar Cipher")
root.configure(bg=BG)
root.resizable(False, False)

# Header
header = tk.Frame(root, bg=WARNA)
header.pack(fill="x")
tk.Label(header, text="CAESAR CIPHER", font=(FONT, 22, "bold"), bg=WARNA, fg="white").pack(pady=(18, 0))
tk.Label(header, text="Cipher substitusi  |  geser tiap huruf sebanyak N posisi",
         font=(FONT, 10), bg=WARNA, fg=MUDA).pack(pady=(2, 18))

# Kartu utama
card = tk.Frame(root, bg="white", padx=22, pady=16)
card.pack(padx=18, pady=18)

label(card, "Teks").pack(anchor="w")
input_text = kotak_teks(card, 5)
input_text.pack(pady=(4, 10))

label(card, "Kunci (angka geser)").pack(anchor="w")
entry_key = tk.Entry(card, font=(FONT, 12), width=8, relief="flat", bg="#F8FAFF",
                     highlightthickness=2, highlightbackground=BORDER, highlightcolor=WARNA)
entry_key.insert(0, "3")
entry_key.pack(anchor="w", pady=(4, 6), ipady=4)
entry_key.bind("<KeyRelease>", update_preview)

# Panel visual khas Caesar: pemetaan alfabet
preview = tk.Label(card, bg=MUDA, fg=GELAP, font=("Consolas", 8), justify="left", padx=8, pady=6)
preview.pack(fill="x", pady=(0, 12))
update_preview()

frame = tk.Frame(card, bg="white")
frame.pack(pady=(0, 12))
tombol(frame, "Enkripsi", lambda: proses(False), WARNA, "white", GELAP).pack(side="left", padx=5)
tombol(frame, "Dekripsi", lambda: proses(True), MUDA, GELAP, "#BFDBFE").pack(side="left", padx=5)

label(card, "Hasil").pack(anchor="w")
output_text = kotak_teks(card, 5)
output_text.pack(pady=(4, 8))

bawah = tk.Frame(card, bg="white")
bawah.pack(fill="x")
status = tk.Label(bawah, text="", bg="white", fg="#64748B", font=(FONT, 9))
status.pack(side="left")
tombol(bawah, "Salin Hasil", salin, "white", WARNA, MUDA).pack(side="right")

root.mainloop()