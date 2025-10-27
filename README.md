# NancyCM – Cookie Maker

**NancyCM** adalah alat berbasis Python yang dirancang untuk menghasilkan **cookie dalam format `username(base64):password(md5)`**, biasanya digunakan dalam skenario autentikasi dasar (Basic Auth) atau dalam pengujian keamanan seperti _brute-force_ atau _password spraying_.

Alat ini mendukung:

- Input **username tunggal**
- Input **password tunggal** atau **daftar password dari file**
- Antarmuka **TUI interaktif** berbasis [Rich](https://github.com/Textualize/rich) (jika tersedia)
- **Fallback ke CLI sederhana** jika Rich tidak terinstal
- Preview proses pembuatan cookie per password (di TUI)
- Konfirmasi overwrite file output
- Penyimpanan hasil ke lokasi yang ditentukan pengguna

---

## 🧠 Cara Kerja

NancyCM bekerja dengan langkah-langkah berikut:

1. **Menerima username** dari pengguna (misal: `wiener`)
2. **Menerima password**:
   - Bisa berupa **satu password** (input langsung), atau
   - **File teks** berisi daftar password (satu per baris)
3. Untuk **setiap password**:
   - Hitung **hash MD5** dari password tersebut
   - Gabungkan menjadi string: `username:md5_hash`
   - Encode string tersebut ke **Base64**
4. Hasil akhir berupa **satu atau banyak cookie** dalam format Base64, siap digunakan sebagai header `Authorization: Basic <cookie>` dalam HTTP request.
5. Simpan semua cookie ke **file output** yang ditentukan pengguna.

Contoh:

- Username: `wiener`
- Password: `peter`
- MD5 dari `peter` = `5f4dcc3b5aa765d61d8327deb882cf99`
- String gabungan: `wiener:5f4dcc3b5aa765d61d8327deb882cf99`
- Base64: `d2llbmVyOjVmNGRkYzNiNWFhNzY1ZDYxZDgzMjdkZWI4ODJjZjk5` ✅

---

## 🚀 Fitur Utama

- ✅ **TUI interaktif** dengan Rich (jika terinstal): tampilan menarik, progress bar, dan preview debug per password
- ✅ **CLI fallback**: tetap berjalan meski tanpa Rich
- ✅ Dukungan **file password** (ideal untuk daftar wordlist)
- ✅ **Expand path otomatis** (misal: `~/passwords.txt` → `/home/user/passwords.txt`)
- ✅ **Konfirmasi overwrite** untuk mencegah kehilangan data
- ✅ Header ASCII opsional dengan `pyfiglet` (jika tersedia)
- ✅ Output **satu cookie per baris**, siap diproses oleh skrip lain

---

## 📁 Struktur Proyek

```
Cookie-Maker/
├── cookie_maker.py       # Program utama
├── requirements.txt      # Dependensi (Rich & pyfiglet opsional)
├── README.md             # Dokumentasi ini
└── image1.png            # Contoh tampilan output
```

---

## ⚙️ Instalasi

1. **Clone repositori**

   ```bash
   git clone https://github.com/username/cookie-maker.git
   cd cookie-maker
   ```

2. **(Opsional) Buat virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   # atau
   venv\Scripts\activate         # Windows
   ```

3. **Instal dependensi**
   ```bash
   pip install -r requirements.txt
   ```
   > Catatan: `rich` dan `pyfiglet` bersifat **opsional**. Jika tidak diinstal, program tetap berjalan dalam mode CLI dasar.

---

## ▶️ Menjalankan Program

### Mode TUI (dengan Rich)

```bash
python cookie_maker.py
```

Ikuti petunjuk interaktif:

1. Masukkan username
2. Pilih mode password: **tunggal** atau **file**
3. Masukkan path file password (jika memilih file)
4. Tentukan lokasi file output
5. Konfirmasi → cookie akan dibuat!

### Mode CLI (tanpa Rich)

Jika `rich` tidak terinstal, program otomatis beralih ke mode CLI sederhana:

```bash
python cookie_maker.py
```

Input dilakukan secara berurutan melalui prompt dasar.

---

## 📌 Contoh Penggunaan

**Input:**

- Username: `wiener`
- File password: `passwords.txt` (berisi `peter`, `admin123`, dll.)
- Output: `~/cookies.txt`

**Output (`cookies.txt`):**

```
d2llbmVyOjVmNGRkYzNiNWFhNzY1ZDYxZDgzMjdkZWI4ODJjZjk5
d2llbmVyOmIyZTdlNjE4ZTQ1ZjQ0YjU5ZjQ1ZjQ0YjU5ZjQ1ZjQ0YjU5
...
```

![Contoh Output](/image1.png)

---

## 🔧 Kustomisasi

- **Ubah lokasi output**: Masukkan path lengkap saat diminta (misal: `/tmp/my_cookies.txt`)
- **Gunakan wordlist besar**: File password bisa berisi ribuan baris — program akan memproses semuanya
- **Nonaktifkan Rich**: Cukup jangan instal `rich`, maka program otomatis pakai CLI

---

## 📄 Lisensi

Proyek ini dirilis di bawah **MIT License** — bebas digunakan, dimodifikasi, dan didistribusikan.
