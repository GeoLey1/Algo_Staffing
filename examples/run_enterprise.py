"""Enterprise-Beispiel: Großes, realistisches Szenario mit 20 Mitarbeitenden und 15 Projekten"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.main import run_optimization


def main():
    print("=" * 80)
    print("ENTERPRISE-SZENARIO")
    print("=" * 80)
    print("\nRealistisches großes Unternehmen:")
    print("  - 20 Mitarbeitende (verschiedene Senioritätsstufen)")
    print("  - 15 Projekte (von KI über Cloud bis Mobile)")
    print("  - 15 Constraints (bevorzugte & ausgeschlossene Zuordnungen)")
    print("  - Mix aus Vollzeit und Teilzeit")
    print("\n")

    summary = run_optimization(
        employees_file=str(project_root / "data" / "enterprise" / "employees.json"),
        projects_file=str(project_root / "data" / "enterprise" / "projects.json"),
        constraints_file=str(project_root / "data" / "enterprise" / "constraints.json"),
        output_file=str(project_root / "output" / "enterprise_results.json")
    )

    print("\n" + "=" * 80)
    print("ANALYSE")
    print("=" * 80)
    print(f"\n  → {len(summary.allocations)} Zuordnungen erstellt")
    print(f"  → {summary.total_employee_utilization:.1f}% Mitarbeiter-Auslastung")
    print(f"  → {summary.total_project_coverage:.1f}% Projekt-Abdeckung")

    if summary.unassigned_employees:
        print(f"\n  ⚠ {len(summary.unassigned_employees)} Mitarbeitende ohne Zuordnung:")
        for emp_id in summary.unassigned_employees[:5]:  # Zeige max 5
            print(f"      - {emp_id}")

    if summary.underallocated_projects:
        print(f"\n  ⚠ {len(summary.underallocated_projects)} Projekte unterbesetzt:")
        for proj_id in summary.underallocated_projects[:5]:
            print(f"      - {proj_id}")

    # Zähle bevorzugte Zuordnungen die erfüllt wurden
    preferred_count = sum(1 for a in summary.allocations if a.is_preferred)
    print(f"\n  ✓ {preferred_count} bevorzugte Zuordnungen wurden berücksichtigt")


if __name__ == "__main__":
    main()
