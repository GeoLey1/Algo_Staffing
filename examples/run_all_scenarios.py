"""Führt alle Beispiel-Szenarien nacheinander aus"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import run_tutorial
import run_enterprise
import run_challenging


def main():
    print("\n" + "🚀" * 40)
    print("ALLE BEISPIEL-SZENARIEN AUSFÜHREN")
    print("🚀" * 40 + "\n")

    scenarios = [
        ("Tutorial", run_tutorial.main),
        ("Enterprise", run_enterprise.main),
        ("Challenging", run_challenging.main)
    ]

    for i, (name, func) in enumerate(scenarios, 1):
        print(f"\n\n{'#' * 80}")
        print(f"# SZENARIO {i}/3: {name}")
        print(f"{'#' * 80}\n")

        try:
            func()
        except Exception as e:
            print(f"\n❌ Fehler beim Ausführen von {name}: {e}")
            continue

        if i < len(scenarios):
            input("\n\n⏸  Drücken Sie Enter für das nächste Szenario...")

    print("\n\n" + "✅" * 40)
    print("ALLE SZENARIEN ABGESCHLOSSEN")
    print("✅" * 40)
    print("\nErgebnisse wurden im output/ Verzeichnis gespeichert:")
    print("  - output/tutorial_results.json")
    print("  - output/enterprise_results.json")
    print("  - output/challenging_results.json")


if __name__ == "__main__":
    main()
