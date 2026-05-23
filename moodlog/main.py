import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, TypedDict

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Tiny CLI to log your mood locally.")
console = Console()

DATA_FILE = Path(os.getenv("MOODLOG_FILE", Path.home() / ".moodlog.json"))

class Entry(TypedDict):
    timestamp: str
    mood: str
    note: str | None

def _load_entries() -> List[Entry]:
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Corrupt data file – expected a list")
            return data
    except json.JSONDecodeError as exc:
        console.print(f"[red]Failed to parse data file:[/red] {exc}")
        sys.exit(1)

def _save_entries(entries: List[Entry]) -> None:
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    except OSError as exc:
        console.print(f"[red]Failed to write data file:[/red] {exc}")
        sys.exit(1)

@app.command()
def add(
    mood: str = typer.Option(..., "--mood", "-m", prompt=True, help="Mood description"),
    note: str = typer.Option("", "--note", "-n", prompt=False, help="Optional free‑form note"),
):
    """Add a new mood entry."""
    entry: Entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mood": mood.strip(),
        "note": note.strip() or None,
    }
    entries = _load_entries()
    entries.append(entry)
    _save_entries(entries)
    console.print("[green]Entry added! 🎉[/green]")

@app.command()
def list(count: int = typer.Option(10, "--count", "-c", help="How many recent entries to show")):
    """List recent mood entries."""
    entries = _load_entries()[-count:][::-1]
    if not entries:
        console.print("[yellow]No entries yet.[/yellow]")
        raise typer.Exit()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Timestamp", style="cyan")
    table.add_column("Mood", style="green")
    table.add_column("Note")
    for idx, e in enumerate(entries, start=1):
        table.add_row(
            str(idx),
            e["timestamp"],
            e["mood"],
            e.get("note") or "-",
        )
    console.print(table)

@app.command()
def stats():
    """Show a simple frequency histogram of moods."""
    from collections import Counter

    entries = _load_entries()
    if not entries:
        console.print("[yellow]No entries to compute statistics.[/yellow]")
        raise typer.Exit()
    counter = Counter(e["mood"] for e in entries)
    max_len = max(len(m) for m in counter)
    total = sum(counter.values())
    for mood, cnt in sorted(counter.items(), key=lambda x: -x[1]):
        bar = "▓" * int((cnt / total) * 20)
        console.print(f"{mood.ljust(max_len)} {bar} ({cnt})")

if __name__ == "__main__":
    app()
