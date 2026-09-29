"""Build the final GreyScienx PDF from report.md."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]
BUILDER = Path(r"C:\Users\Deriv\Documents\ChatGPT\GreySciencx\.agents\skills\greyscienx-editorial-pdf\scripts\build_report.py")
OUTPUT = WORKSPACE / "research" / "publications" / "the-first-three-years-advantage.pdf"

command = [
    sys.executable,
    str(BUILDER),
    str(ROOT / "report.md"),
    str(OUTPUT),
    "--css",
    str(WORKSPACE / "app" / "globals.css"),
    "--title",
    "The First Three Years Advantage",
    "--subtitle",
    "How much can three boring years in your twenties change the next forty?",
    "--title-accent",
    "Three Years",
    "--eyebrow",
    "GreyScienx / Household finance",
    "--meta",
    "GreyScienx | Research publication | September 2026 | Constant 2026 rand",
    "--header-title",
    "The First Three Years Advantage",
    "--footer-meta",
    "GreyScienx | September 2026 | Scenario research",
    "--author",
    "GreyScienx",
    "--subject",
    "South African household independence, vehicle ownership and lifetime wealth",
    "--cover-stat",
    "R602k|CENTRAL AGE-25 ADVANTAGE",
    "--cover-stat",
    "R3.32m|CENTRAL AGE-60 DIFFERENCE",
    "--cover-stat",
    "54|STRATEGY-CITY-SALARY CASES",
]

subprocess.run(command, check=True, cwd=WORKSPACE)
print(OUTPUT)
