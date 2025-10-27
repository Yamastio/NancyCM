from __future__ import annotations
import os
import sys
import hashlib
import base64
from pathlib import Path
from typing import List

# Optional dependencies
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.progress import track
    from rich.text import Text

    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    console = None  # type: ignore
    RICH_AVAILABLE = False

try:
    import pyfiglet
    FIGLET_AVAILABLE = True
except ImportError:
    FIGLET_AVAILABLE = False


# =========================
# Utility functions
# =========================

def md5_of(s: str) -> str:
    """Return the MD5 hash of a string."""
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def make_cookie(username: str, password: str) -> str:
    """Return cookie in format username(base64):password(md5)."""
    hashed = md5_of(password)
    raw = f"{username}:{hashed}"
    return base64.b64encode(raw.encode("utf-8")).decode("ascii")


def safe_expand_path(p: str) -> str:
    """Expand ~ and normalize path."""
    return str(Path(p.strip()).expanduser().resolve())


def read_lines_from_file(path: str) -> List[str]:
    """Read non-empty lines from a file."""
    path_obj = Path(safe_expand_path(path))
    if not path_obj.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    with path_obj.open("r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


# =========================
# TUI / CLI helpers
# =========================

def header() -> None:
    title = "Cookie Maker"
    subtitle = "username(base64):password(md5)"
    if FIGLET_AVAILABLE:
        art = pyfiglet.figlet_format(title, font="slant")
        if RICH_AVAILABLE:
            console.print(Panel.fit(Text(art, style="bold green"),
                          subtitle=subtitle, padding=(1, 2)))
        else:
            print(art)
            print(subtitle)
    else:
        if RICH_AVAILABLE:
            console.print(
                Panel.fit(f"[bold green]{title}[/bold green]\n{subtitle}", padding=(1, 2)))
        else:
            print(f"=== {title} ===")
            print(subtitle)


def prompt_input(prompt_text: str, default: str | None = None) -> str:
    if RICH_AVAILABLE:
        return Prompt.ask(prompt_text, default=default) if default else Prompt.ask(prompt_text)
    else:
        val = input(f"{prompt_text}{f' [{default}]' if default else ''}: ")
        return val.strip() or (default if default else "")


def confirm(prompt: str = "Are you sure?") -> bool:
    if RICH_AVAILABLE:
        return Confirm.ask(prompt)
    else:
        resp = input(f"{prompt} [y/N]: ").strip().lower()
        return resp in ("y", "yes")


def display_list(name: str, items: List[str]) -> None:
    if RICH_AVAILABLE:
        table = Table(show_header=False)
        for i, item in enumerate(items, start=1):
            table.add_row(str(i), item)
        console.print(Panel(table, title=name, padding=(1, 1)))
    else:
        print(f"--- {name} ---")
        for i, item in enumerate(items, start=1):
            print(f"{i:3d}. {item}")
        print("-" * 20)


# =========================
# Core functionality
# =========================

def generate_cookies(username: str, passwords: List[str], output_path: str) -> int:
    """Generate cookies and write to file. Returns number of cookies."""
    out_path = Path(safe_expand_path(output_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cookies: List[str] = []
    if RICH_AVAILABLE:
        console.print("\n[bold green]Processing...[/bold green]")
        for pw in track(passwords, description="Converting"):
            c = make_cookie(username, pw)
            cookies.append(c)
            console.print(
                f"[dim]{pw}[/dim] -> md5: [magenta]{md5_of(pw)}[/magenta] -> cookie: [cyan]{c}[/cyan]")
    else:
        print("\nProcessing...")
        for pw in passwords:
            c = make_cookie(username, pw)
            cookies.append(c)
            print(f"{pw} -> {md5_of(pw)} -> {c}")

    with out_path.open("w", encoding="utf-8") as f:
        for c in cookies:
            f.write(c + "\n")

    return len(cookies)


# =========================
# Main program loop
# =========================

def main_loop() -> None:
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        header()

        username = prompt_input(
            "Enter username (single username, e.g., wiener)")

        # Password mode
        if RICH_AVAILABLE:
            console.print(
                "\n[bold]Password input mode:[/bold] (1) Single password  (2) Password list file")
            mode_choice = Prompt.ask("Choose mode", choices=[
                                     "1", "2"], default="2")
            pw_mode = "file" if mode_choice == "2" else "single"
        else:
            mode_choice = input(
                "Password mode: (1) Single (2) File [default 2]: ").strip() or "2"
            pw_mode = "file" if mode_choice == "2" else "single"

        passwords: List[str] = []
        if pw_mode == "single":
            passwords = [prompt_input("Enter password (can be empty)")]
        else:
            while True:
                try:
                    pw_file = prompt_input(
                        "Enter password file path (one per line, e.g., ~/passwords.txt)")
                    passwords = read_lines_from_file(pw_file)
                    break
                except FileNotFoundError as e:
                    if RICH_AVAILABLE:
                        console.print(f"[red]Error:[/red] {e}")
                    else:
                        print("Error:", e)

        out_path = prompt_input(
            "Enter output path and filename (e.g., ~/cookies.txt)", default="~/cookies.txt")

        # Summary
        if RICH_AVAILABLE:
            console.print(Panel.fit(
                f"[bold]Summary[/bold]\nUsername: [cyan]{username}[/cyan]\nPasswords: [yellow]{len(passwords)}[/yellow]\nOutput: [green]{out_path}[/green]", subtitle="Confirm before processing", padding=(1, 2)))
        else:
            print(
                f"\nSummary:\n Username: {username}\n Password count: {len(passwords)}\n Output: {out_path}")

        if not confirm("Proceed and generate cookies?"):
            print("Cancelled. Returning to input...")
            input("Press Enter to continue...")
            continue

        if Path(out_path).exists() and not confirm(f"File {out_path} exists. Overwrite?"):
            print("Aborted by user. Returning to input...")
            input("Press Enter to continue...")
            continue

        try:
            count = generate_cookies(username, passwords, out_path)
            if RICH_AVAILABLE:
                console.print(Panel.fit(
                    f"[bold green]Success[/bold green]\nWrote {count} cookies to:\n[green]{out_path}[/green]"))
            else:
                print(f"\nSuccess: wrote {count} cookies to {out_path}")
        except Exception as e:
            if RICH_AVAILABLE:
                console.print(f"[red]Error writing file:[/red] {e}")
            else:
                print("Error writing file:", e)

        if not confirm("Do you want to generate another batch?"):
            print("Goodbye")
            break


if __name__ == "__main__":
    try:
        if RICH_AVAILABLE:
            main_loop()
        else:
            # fallback simple run
            from sys import exit
            print("Cookie Maker (basic mode)")
            username = input("Username: ").strip()
            mode = input(
                "Password mode - single/file? [file]: ").strip().lower() or "file"
            passwords = [input("Password: ")] if mode.startswith(
                "s") else read_lines_from_file(input("Password file path: ").strip())
            out_path = safe_expand_path(
                input("Output path [~/cookies.txt]: ").strip() or "~/cookies.txt")
            print(f"Generating {len(passwords)} cookies to {out_path}...")
            count = generate_cookies(username, passwords, out_path)
            print(f"Done. Wrote {count} cookies to {out_path}")
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print("\n[red]Interrupted by user[/red]")
        else:
            print("\nInterrupted by user")
        sys.exit(1)
