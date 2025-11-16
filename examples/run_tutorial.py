"""Tutorial-Beispiel: Kleines, einfaches Szenario zum Kennenlernen"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.main import run_optimization


def main():
    print("=" * 80)
    print("TUTORIAL-SZENARIO")
    print("=" * 80)
    print("\nDieses einfache Beispiel hilft Ihnen, das System kennenzulernen:")
    print("  - 3 Mitarbeitende (Senior, Intermediate, Junior)")
    print("  - 3 Projekte mit unterschiedlichen Anforderungen")
    print("  - 1 bevorzugte Zuordnung")
    print("\n")

    summary = run_optimization(
        employees_file=str(project_root / "data" / "tutorial" / "employees.json"),
        projects_file=str(project_root / "data" / "tutorial" / "projects.json"),
        constraints_file=str(project_root / "data" / "tutorial" / "constraints.json"),
        output_file=str(project_root / "output" / "tutorial_results.json")
    )

    print("\n" + "=" * 80)
    print("ANALYSE")
    print("=" * 80)
    print("\nWas können wir lernen?")
    print("  ✓ Lisa wird optimal auf das Backend-Projekt zugeordnet (bevorzugt)")
    print("  ✓ Tom deckt die Datenanalyse ab")
    print("  ✓ Sarah (Teilzeit 50%) wird für das Frontend eingeplant")
    print(f"\n  → {summary.total_employee_utilization:.1f}% der verfügbaren Kapazität wurde genutzt")
    print(f"  → {summary.total_project_coverage:.1f}% der Projekt-Anforderungen wurden erfüllt")


if __name__ == "__main__":
    main()
