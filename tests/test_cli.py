from pathlib import Path
import os
import json
import subprocess
import sys

# Use a temporary directory for the data file to avoid polluting the real home dir
TMP_DIR = Path(__file__).parent / "tmp"
TMP_DIR.mkdir(exist_ok=True)
DATA_FILE = TMP_DIR / "moodlog.json"

# Ensure the CLI sees the custom path via env var
env = os.environ.copy()
env["MOODLOG_FILE"] = str(DATA_FILE)

def run_cli(*args):
    cmd = [sys.executable, "-m", "moodlog.main"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result

def test_add_and_list():
    # Clean start
    if DATA_FILE.exists():
        DATA_FILE.unlink()

    # Add a mood entry (non‑interactive mode using Typer's automatic prompts is tricky,
    # so we invoke the command with explicit options)
    res = run_cli("add", "--mood", "happy", "--note", "testing")
    assert res.returncode == 0
    assert "Entry added" in res.stdout

    # List entries and verify output contains our data
    res = run_cli("list", "--count", "1")
    assert res.returncode == 0
    assert "happy" in res.stdout
    assert "testing" in res.stdout

def test_stats_output():
    # Ensure there is at least one entry
    if not DATA_FILE.exists():
        run_cli("add", "--mood", "neutral")

    res = run_cli("stats")
    assert res.returncode == 0
    # The output should contain a histogram bar and a count
    assert "(" in res.stdout and ")" in res.stdout
