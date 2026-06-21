import base64
import codecs
import re
import urllib.parse
import sys
import os
import string
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_multiline_input(title, prompt_text, style="cyan"):
    console.print() 
    content = f"[bold yellow]{prompt_text}[/bold yellow]\n[dim white]ℹ️  Press ENTER twice on an empty line to confirm and execute.[/dim white]"
    input_panel = Panel(
        content, 
        title=f"[bold {style}]{title}[/bold {style}]", 
        border_style=style, 
        expand=False 
    )
    console.print(input_panel)
    lines = []
    while True:
        try:
            line = input()
            if len(line) > 20000: line = line[:20000]
            if line == "": break
            lines.append(line)
        except EOFError: break
    return "\n".join(lines).strip()

def is_human_readable(byte_data):
    try:
        text = byte_data.decode('utf-8')
        if not text.strip(): return False, ""
        valid_chars = set(string.printable)
        printable_count = sum(1 for c in text if c in valid_chars or c.isprintable())
        if printable_count / len(text) > 0.80: return True, text
        return False, ""
    except Exception: return False, ""

def print_banner():
    clear_screen()
    banner = """
 ____            ____            _      __  __ 
|  _ \  ___     / ___|___    __| | ___ \ \/ / 
| | | |/ _ \   | |   / _ \  / _` |/ _ \ \  /  
| |_| |  __/   | |__| (_) || (_| |  __/ /  \  
|____/ \___|___\____\___/  \__,_|\___|/_/\_\ 
           |_____|                            
    """
    console.print(banner, style="bold green", justify="center")
    console.print("[bold cyan]Advanced Auto-Detection Engine[/bold cyan]", justify="center")
    console.print("[bold yellow]Created by: Reyep[/bold yellow]\n", justify="center")

def print_goodbye():
    console.print("\n[bold yellow]Exiting De-CodeX...[/bold yellow]")
    console.print("[bold cyan]Tool created by: Reyep[/bold cyan]")
    console.print("[bold yellow]Hope to see you soon! 👋[/bold yellow]\n")

def auto_decode(data):
    data = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', data.strip().replace("│", "").replace("┃", ""))
    clean_rigid = data.replace("\n", "").replace("\r", "").replace(" ", "")
    clean_text = data.replace("\n", "").replace("\r", "")

    if re.match(r'^[01\s]+$', data) and len(clean_rigid) % 8 == 0 and len(clean_rigid) > 0:
        try:
            bytes_data = int(clean_rigid, 2).to_bytes(len(clean_rigid) // 8, byteorder='big')
            valid, text = is_human_readable(bytes_data)
            if valid: return "Binary Code", text
        except: pass

    if re.match(r'^[0-7\s]+$', data) and len(data.split()) > 0:
        try:
            decoded_oct = ''.join(chr(int(c, 8)) for c in data.split())
            valid, text = is_human_readable(decoded_oct.encode('utf-8'))
            if valid: return "Octal", text
        except: pass

    if re.match(r'^[a-fA-F0-9]{32}$', clean_rigid):
        return "MD5 Hash", "N/A (Hashes are one-way, but now you know it's MD5!)"
    if re.match(r'^[a-fA-F0-9]{64}$', clean_rigid):
        return "SHA-256 Hash", "N/A (Hashes are one-way, but now you know it's SHA-256!)"

    hex_pure = clean_rigid.replace("0x", "")
    if re.match(r'^[a-fA-F0-9]+$', hex_pure) and len(hex_pure) % 2 == 0 and len(hex_pure) >= 4:
        try:
            decoded_bytes = bytes.fromhex(hex_pure)
            valid, text = is_human_readable(decoded_bytes)
            if valid: return "Hexadecimal (HEX)", text
        except: pass

    try:
        decoded_bytes = base64.b85decode(clean_rigid)
        valid, text = is_human_readable(decoded_bytes)
        if valid: return "Base85", text
    except: pass

    try:
        decoded_bytes = base64.b64decode(clean_rigid, validate=True)
        valid, text = is_human_readable(decoded_bytes)
        if valid: return "Base64", text
    except: pass

    if "%" in clean_text and re.search(r'%[0-9a-fA-F]{2}', clean_text):
        try:
            decoded_url = urllib.parse.unquote(clean_text)
            if decoded_url != clean_text: return "URL Encoded", decoded_url
        except: pass

    if any(c.isalpha() for c in clean_text) and " " in data:
        return "ROT13 (Caesar Cipher)", codecs.encode(clean_text, 'rot_13')

    return "Unknown / Not a supported cipher", "Could not decode. Data might be corrupted or plaintext."

def encode_data(text, choice):
    encode_map = {
        "1": ("Base64", lambda t: base64.b64encode(t.encode('utf-8')).decode('utf-8')),
        "2": ("Base32", lambda t: base64.b32encode(t.encode('utf-8')).decode('utf-8')),
        "3": ("Base85", lambda t: base64.b85encode(t.encode('utf-8')).decode('utf-8')),
        "4": ("Binary Code", lambda t: ' '.join(format(byte, '08b') for byte in t.encode('utf-8'))),
        "5": ("Octal", lambda t: ' '.join(oct(byte)[2:].zfill(3) for byte in t.encode('utf-8'))),
        "6": ("Hexadecimal (HEX)", lambda t: t.encode('utf-8').hex()),
        "7": ("URL Encoded", lambda t: urllib.parse.quote(t)),
        "8": ("ROT13 (Caesar Cipher)", lambda t: codecs.encode(t, 'rot_13'))
    }
    if choice in encode_map:
        return encode_map[choice]
    return None, None

def main():
    print_banner()
    while True:
        try:
            console.print("[bold cyan]==============================================[/bold cyan]")
            console.print("[bold magenta]1.[/bold magenta] 🔒 Encode")
            console.print("[bold cyan]2.[/bold cyan] 🔓 Auto-Decode")
            console.print("[bold red]3.[/bold red] ❌ Exit\n")
            mode = console.input("[bold yellow]Select an option (1-3): [/bold yellow]").strip()
            
            if mode == "1":
                console.print("\n[bold magenta]--- Available Encoding Methods ---[/bold magenta]")
                console.print("[bold white][1][/bold white] Base64")
                console.print("[bold white][2][/bold white] Base32")
                console.print("[bold white][3][/bold white] Base85")
                console.print("[bold white][4][/bold white] Binary Code")
                console.print("[bold white][5][/bold white] Octal")
                console.print("[bold white][6][/bold white] Hexadecimal (HEX)")
                console.print("[bold white][7][/bold white] URL Encoding")
                console.print("[bold white][8][/bold white] ROT13 (Caesar Cipher)\n")
                
                method = console.input("[bold yellow]Choose encryption method (1-8): [/bold yellow]").strip()
                if method not in [str(i) for i in range(1, 9)]:
                    console.print("[bold red]Invalid selection![/bold red]\n")
                    continue
                
                plain_text = get_multiline_input("🔒 ENCRYPTION INPUT", "Write or Paste the text to encrypt:", style="magenta")
                if not plain_text: continue
                
                cipher_type, encode_func = encode_data(plain_text, method)
                result = encode_func(plain_text)
                
                table = Table(title="De-CodeX Results", title_style="bold underline magenta")
                table.add_column("Property", style="magenta", no_wrap=True)
                table.add_column("Value", style="green", overflow="fold", no_wrap=False, ratio=1)
                table.add_row("Chosen Method", cipher_type)
                table.add_row("Encoded Output", result)
                
                console.print("\n", Panel(table, expand=True, border_style="bold magenta"))
                console.print(f"\n[bold yellow]📋 Clean Output:[/bold yellow]\n{result}\n")
                
            elif mode == "2":
                secret = get_multiline_input("🔓 DECRYPTION INPUT", "Write or Paste the mysterious string to analyze:", style="cyan")
                if not secret: continue
                
                with console.status("[bold green]Analyzing and cracking...[/bold green]"):
                    cipher_type, result = auto_decode(secret)
                
                table = Table(title="De-CodeX Results", title_style="bold underline cyan")
                table.add_column("Property", style="cyan", no_wrap=True)
                table.add_column("Value", style="green", overflow="fold", no_wrap=False, ratio=1)
                table.add_row("Detected Cipher", cipher_type)
                table.add_row("Decoded Output", result)
                
                console.print("\n", Panel(table, expand=True, border_style="bold cyan"))
                console.print(f"\n[bold yellow]📋 Clean Output:[/bold yellow]\n{result}\n")

            elif mode == "3":
                print_goodbye()
                sys.exit(0)
            else:
                console.print("[bold red]Invalid option. Please choose 1, 2, or 3.[/bold red]\n")
                
        except KeyboardInterrupt:
            print_goodbye()
            sys.exit(0)

if __name__ == "__main__":
    main()
