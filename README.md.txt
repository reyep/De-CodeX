# De-CodeX v1.0 🚀

De-CodeX is a simple, interactive, and useful Command Line Interface (CLI) tool written in Python for automated string encoding and decoding. It is designed for cybersecurity professionals, CTF players, and developers who need quick and smart cipher analysis.

Equipped with an intelligent detection engine, De-CodeX automatically identifies the underlying encoding or cipher of a mysterious string and cracks it instantly.

## 🌟 Features

* **Interactive CLI Menu:** Clean terminal UI powered by the `rich` library.
* **Smart Auto-Decoding:** Automatically detects and decodes:
  * Binary Code
  * Hashes (Identifies MD5 & SHA-256)
  * Hexadecimal (HEX)
  * URL Encoding
  * Base64
  * ROT13 (Caesar Cipher) as fallback
* **Clean Output for Copying:** Generates detailed tables but also prints a raw text line below for a perfect copy-paste experience, preventing annoying whitespace issues.

## 🛠️ Installation & Setup

De-CodeX has been tested and is designed to run exclusively on Linux.

### 1. Clone the repository
Open your terminal and run:
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/De-CodeX.git](https://github.com/YOUR_GITHUB_USERNAME/De-CodeX.git)
cd De-CodeX