# NancyCM

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Rich](https://img.shields.io/badge/Rich-TUI-green.svg)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**NancyCM** adalah alat berbasis Python untuk membuat **cookie dalam format `username(base64):password(md5)`**.
Mendukung input **single username** atau **daftar password dari file**, dan menawarkan **TUI interaktif** menggunakan [Rich](https://github.com/Textualize/rich) atau fallback **CLI sederhana** jika Rich tidak tersedia.

---

## Key Features

- Input username tunggal
- Input password tunggal atau dari file (satu password per baris)
- Generate cookie: `username(base64):password(md5)`
- TUI interaktif dengan preview progress dan debug per password
- Fallback CLI sederhana bila Rich tidak tersedia
- Output tersimpan sesuai path yang ditentukan
- Konfirmasi sebelum overwrite file

---

## Project Structure

```
Cookie-Maker/
├── cookie_maker.py       # Main program
├── requirements.txt      # Dependencies
├── README.md             # This documentation
└── image1.png            # Contoh screenshot / preview
```

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/username/cookie-maker.git
cd cookie-maker
```

2. **Create a virtual environment** (optional but recommended)

```bash
python -m venv venv
jsource venv/bin/activate      # Bash/Zsh
# or
venv\Scripts\activate         # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Running Cookie Maker

- **TUI interface (with Rich)**

```bash
python cookie_maker.py

```

Steps:

1. Enter username
2. Select password mode: single or file
3. Enter password file path (if file)
4. Enter output path
5. Confirm to generate cookies

- **CLI fallback (without Rich)**

```bash
python cookie_maker.py
```

Steps:

1. Enter username
2. Enter password or file password
3. Enter output path
4. Confirm to generate cookies

> **Note:** CLI fallback mode is automatically activated if Rich is not installed.

---

## Example Usage

```
Username: wiener
Password file: passwords.txt
Output file: ~/cookies.txt
```

Generated cookie example:

```
d2llbmVyOjVmNGRkYzNiNWFhNzY1ZDYxZDgzMjdkZWI4ODJjZjk5
```

![Example Output](/image1.png)

---

## Customization

### 1. Output file path

Change the default output path in prompt or set a custom one.

### 2. Password input mode

Switch between **single password** or **password list file**.

### 3. Display / progress

- TUI mode shows live progress and debug info
- CLI mode prints basic info to terminal

---

## Dependencies

See `requirements.txt`:

- `rich` (optional, for TUI)
- `pyfiglet` (optional, for ASCII header)

> If dependencies are not installed, the program falls back to simple CLI mode.

---

## License

This project is open source under **MIT License** — feel free to use, modify, and contribute.
