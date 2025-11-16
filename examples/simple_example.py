"""Einfaches Beispiel für die Nutzung des Resource Allocation Optimizers"""

import sys
from pathlib import Path

# Füge src zum Python-Pfad hinzu
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.main import run_optimization


def main():
    """Führt eine einfache Optimierung mit den Beispieldaten durch"""

    print("Resource Allocation Optimizer - Beispiel")
    print("=" * 80)

    # Optimierung mit Standardgewichtungen durchführen
    summary = run_optimization(
        employees_file=str(project_root / "data" / "employees.json"),
        projects_file=str(project_root / "data" / "projects.json"),
        constraints_file=str(project_root / "data" / "constraints.json"),
        output_file=str(project_root / "output" / "allocation_results.json"),
        utilization_weight=40.0,    # 40% Gewichtung für Auslastung
        skill_match_weight=40.0,    # 40% Gewichtung für Skill-Match
        priority_weight=15.0,       # 15% Gewichtung für Projekt-Priorität
        preference_weight=5.0       # 5% Gewichtung für Präferenzen
    )

    print("\n✅ Optimierung erfolgreich abgeschlossen!")
    print(f"   {summary.total_allocations} Zuordnungen erstellt")
    print(f"   {summary.total_employee_utilization:.1f}% Mitarbeiter-Auslastung")
    print(f"   {summary.total_project_coverage:.1f}% Projekt-Abdeckung")


if __name__ == "__main__":
    main()
