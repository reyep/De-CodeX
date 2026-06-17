import base64
import codecs
import re
import urllib.parse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def print_banner():
    banner = r"""
 ____           ____          _      __  __ 
|  _ \  ___    / ___|___   __| | ___ \ \/ / 
| | | |/ _ \  | |   / _ \ / _` |/ _ \ \  /  
| |_| |  __/  | |__| (_) | (_| |  __/ /  \  
|____/ \___|___\____\___/ \__,_|\___|/_/\_\ 
          |_____|                           
    [bold cyan]v1.0 - Professional Encoder & Auto-Decoder CLI[/bold cyan]
    [bold yellow]Created by: Reyep[/bold yellow]
    """
    console.print(banner, style="bold green")

def auto_decode(data):
    data = data.strip().replace("│", "").replace("┃", "")
    clean_rigid = data.replace("\n", "").replace("\r", "").replace(" ", "")
    clean_text = data.replace("\n", "").replace("\r", "")

    if re.match(r'^[01]+$', clean_rigid) and len(clean_rigid) % 8 == 0 and len(clean_rigid) > 0:
        try:
            bytes_data = int(clean_rigid, 2).to_bytes(len(clean_rigid) // 8, byteorder='big')
            return "Binary Code", bytes_data.decode('utf-8')
        except Exception:
            pass

    if re.match(r'^[a-fA-F0-9]{32}$', clean_rigid):
        return "MD5 Hash", "N/A (Hashes are one-way, but now you know it's MD5!)"
    if re.match(r'^[a-fA-F0-9]{64}$', clean_rigid):
        return "SHA-256 Hash", "N/A (Hashes are one-way, but now you know it's SHA-256!)"

    hex_pure = clean_rigid.replace("0x", "")
    if re.match(r'^[a-fA-F0-9]+$', hex_pure) and len(hex_pure) % 2 == 0 and len(hex_pure) >= 4:
        try:
            decoded_hex = bytes.fromhex(hex_pure).decode('utf-8')
            if decoded_hex.isprintable(): 
                return "Hexadecimal (HEX)", decoded_hex
        except Exception:
            pass

    if "%" in clean_text and re.search(r'%[0-9a-fA-F]{2}', clean_text):
        try:
            decoded_url = urllib.parse.unquote(clean_text)
            if decoded_url != clean_text:
                return "URL Encoded", decoded_url
        except Exception:
            pass

    if re.match(r'^[a-zA-Z0-9+/]+={0,2}$', clean_rigid) and len(clean_rigid) % 4 == 0 and len(clean_rigid) >= 4:
        try:
            decoded_bytes = base64.b64decode(clean_rigid, validate=True)
            return "Base64", decoded_bytes.decode('utf-8')
        except Exception:
            pass

    if any(c.isalpha() for c in clean_text):
        rot13_attempt = codecs.encode(clean_text, 'rot_13')
        return "ROT13 (Caesar Cipher)", rot13_attempt

    return "Unknown / Cipher not supported yet", "Could not decode."

def encode_data(text, choice):
    if choice == "1":    
        return "Base64", base64.b64encode(text.encode('utf-8')).decode('utf-8')
    elif choice == "2":  
        return "Binary Code", ' '.join(format(byte, '08b') for byte in text.encode('utf-8'))
    elif choice == "3":  
        return "Hexadecimal (HEX)", text.encode('utf-8').hex()
    elif choice == "4":  
        return "URL Encoded", urllib.parse.quote(text)
    elif choice == "5":  
        return "ROT13 (Caesar Cipher)", codecs.encode(text, 'rot_13')
    return None, None

def main():
    print_banner()
    while True:
        try:
            console.print("\n[bold cyan]==============================================[/bold cyan]")
            console.print("[bold white][1][/bold white] 🔒 Encode")
            console.print("[bold white][2][/bold white] 🔓 Auto-Decode")
            console.print("[bold white][3][/bold white] ❌ Exit\n")
            mode = console.input("[bold yellow]Select an option (1-3): [/bold yellow]").strip()
            
            if mode == "1":
                console.print("\n[bold cyan]--- Available Encoding Methods ---[/bold cyan]")
                console.print("[bold white][1][/bold white] Base64\n[bold white][2][/bold white] Binary Code\n[bold white][3][/bold white] Hexadecimal (HEX)\n[bold white][4][/bold white] URL Encoding\n[bold white][5][/bold white] ROT13 (Caesar Cipher)\n")
                method = console.input("[bold yellow]Choose encryption method (1-5): [/bold yellow]").strip()
                if method not in ["1", "2", "3", "4", "5"]:
                    continue
                plain_text = console.input("\n[bold yellow]Enter the text you want to encrypt: [/bold yellow]")
                if not plain_text: continue
                cipher_type, result = encode_data(plain_text, method)
                table = Table(title="De-CodeX Encryption Results", title_style="bold underline magenta")
                table.add_column("Property", style="cyan", no_wrap=True)
                table.add_column("Value", style="green", overflow="fold", no_wrap=False, ratio=1)
                table.add_row("Chosen Method", cipher_type)
                table.add_row("Encoded Output", result)
                console.print("\n", Panel(table, expand=True, border_style="bold green"))
                console.print("\n[bold yellow]📋 Clean Output for Copy (Triple-click line below):[/bold yellow]\n", result)
                
            elif mode == "2":
                secret = console.input("\n[bold yellow]Enter the mysterious string to analyze: [/bold yellow]")
                if not secret: continue
                with console.status("[bold green]Analyzing and cracking...[/bold green]"):
                    cipher_type, result = auto_decode(secret)
                table = Table(title="De-CodeX Decryption Results", title_style="bold underline magenta")
                table.add_column("Property", style="cyan", no_wrap=True)
                table.add_column("Value", style="green", overflow="fold", no_wrap=False, ratio=1)
                table.add_row("Detected Cipher", cipher_type)
                table.add_row("Decoded Output", result)
                console.print("\n", Panel(table, expand=True, border_style="bold blue"))
                console.print("\n[bold yellow]📋 Clean Output for Copy (Triple-click line below):[/bold yellow]\n", result)

            elif mode == "3":
                console.print("\n[yellow]Exiting De-CodeX... Goodbye![/yellow]\n")
                sys.exit(0)
        except KeyboardInterrupt:
            console.print("\n\n[bold red][!] Interrupted by user (Ctrl+C)[/bold red]\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
