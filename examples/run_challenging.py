"""Challenging-Beispiel: Schwieriges Szenario mit vielen Constraints und Edge Cases"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.main import run_optimization


def main():
    print("=" * 80)
    print("CHALLENGING-SZENARIO")
    print("=" * 80)
    print("\nDieses Szenario zeigt, wie der Optimizer mit Herausforderungen umgeht:")
    print("  - Viele Teilzeit-Mitarbeitende (30%-80% Verfügbarkeit)")
    print("  - Skill-Mismatches (nicht alle Projekte haben passende Experten)")
    print("  - Hohe Seniority-Anforderungen bei wenig Senior-Kapazität")
    print("  - Überbuchung (mehr Projekt-Bedarf als verfügbare Kapazität)")
    print("\n")

    summary = run_optimization(
        employees_file=str(project_root / "data" / "challenging" / "employees.json"),
        projects_file=str(project_root / "data" / "challenging" / "projects.json"),
        constraints_file=str(project_root / "data" / "challenging" / "constraints.json"),
        output_file=str(project_root / "output" / "challenging_results.json")
    )

    print("\n" + "=" * 80)
    print("ANALYSE DER HERAUSFORDERUNGEN")
    print("=" * 80)

    print(f"\n  → {summary.total_employee_utilization:.1f}% Auslastung erreicht")
    print(f"  → {summary.total_project_coverage:.1f}% Projekt-Abdeckung")

    if summary.total_project_coverage < 100:
        print("\n  ⚠ Nicht alle Projekte konnten vollständig besetzt werden!")
        print("     Gründe könnten sein:")
        print("     - Zu wenig verfügbare Kapazität (viele Teilzeit)")
        print("     - Skill-Mismatch (fehlende Experten)")
        print("     - Seniority-Constraints nicht erfüllbar")

    if summary.unassigned_employees:
        print(f"\n  ⚠ {len(summary.unassigned_employees)} Mitarbeitende ohne Projekt:")
        for emp_id in summary.unassigned_employees:
            print(f"      - {emp_id}")
        print("     → Deren Skills passen zu keinem Projekt")

    if summary.underallocated_projects:
        print(f"\n  ⚠ {len(summary.underallocated_projects)} unterbesetzte Projekte:")
        for proj_id in summary.underallocated_projects:
            print(f"      - {proj_id}")

    print("\n" + "=" * 80)
    print("EMPFEHLUNGEN")
    print("=" * 80)
    print("\n  Bei solchen Herausforderungen können Sie:")
    print("    1. Projekt-Prioritäten anpassen (wichtige Projekte zuerst)")
    print("    2. Gewichtungen ändern (z.B. mehr Fokus auf Projekt-Coverage)")
    print("    3. Externe Ressourcen einplanen")
    print("    4. Projekt-Scope reduzieren oder Timeline anpassen")


if __name__ == "__main__":
    main()
