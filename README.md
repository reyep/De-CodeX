# De-CodeX v1.0

De-CodeX is a robust, interactive, and optimized CLI (Command Line Interface) tool written in Python, designed for automated string encoding and decoding. Built for cybersecurity professionals, CTF players, and developers who require fast and precise cipher analysis.

Equipped with an intelligent detection engine, De-CodeX automatically identifies the underlying encoding of a mysterious string and decrypts it instantly, providing a clean and secure user experience.

## 🌟 Key Features

* **Smart Auto-Detection Engine:** Automatically identifies a wide range of ciphers and encodings.
* **Integrated Security (v1.0):** Implements input sanitization, memory management, and process isolation to prevent crashes and unexpected errors.
* **Elegant Interface:** Interactive UI built with the `rich` library for clear and professional navigation.
* **Multi-Cipher Support:**
    * Base64, Base32, Base85, Ascii85
    * Binary and Octal encoding
    * Hexadecimal (HEX)
    * URL Encoding
    * ROT13 (Caesar Cipher)
* **Hash Detection:** Immediate identification of MD5 and SHA-256.
* **Optimized Output:** Detailed results displayed in tables, with a dedicated "Clean Output" line below for instant copy-pasting.

## 🛠️ Installation & Setup

De-CodeX is designed to be lightweight and cross-platform.

### Prerequisites

Make sure you have Python 3.x installed. The tool requires the `rich` library for the graphical interface.

```bash
pip install rich
```

### Cloning the repository
Clone the repository using the terminal:


```bash
git clone [https://github.com/reyep/De-CodeX.git](https://github.com/reyep/De-CodeX.git)

cd De-CodeX
```

### Run the tool
Start the engine by running:

```bash
python3 decodex.py
```

### 🔒 Security Note

This is the first stable release (v1.0). We have introduced rigorous security checks to ensure the tool can be used in complex analysis environments without the risk of injections or memory exhaustion. This tool is intended for educational purposes, research, and CTF challenges.