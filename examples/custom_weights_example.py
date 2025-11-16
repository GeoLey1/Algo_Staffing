"""Beispiel mit angepassten Gewichtungen für verschiedene Optimierungsziele"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.main import run_optimization


def scenario_maximize_utilization():
    """Szenario: Maximiere Mitarbeiter-Auslastung (wichtiger als Skill-Match)"""
    print("\n" + "=" * 80)
    print("SZENARIO 1: Maximale Auslastung")
    print("=" * 80)

    run_optimization(
        employees_file=str(project_root / "data" / "employees.json"),
        projects_file=str(project_root / "data" / "projects.json"),
        constraints_file=str(project_root / "data" / "constraints.json"),
        output_file=str(project_root / "output" / "scenario_max_utilization.json"),
        utilization_weight=70.0,    # Hohe Gewichtung für Auslastung
        skill_match_weight=20.0,    # Niedrigere Gewichtung für Skill-Match
        priority_weight=8.0,
        preference_weight=2.0
    )


def scenario_perfect_skill_match():
    """Szenario: Optimale Skill-Besetzung (wichtiger als Auslastung)"""
    print("\n" + "=" * 80)
    print("SZENARIO 2: Perfekter Skill-Match")
    print("=" * 80)

    run_optimization(
        employees_file=str(project_root / "data" / "employees.json"),
        projects_file=str(project_root / "data" / "projects.json"),
        constraints_file=str(project_root / "data" / "constraints.json"),
        output_file=str(project_root / "output" / "scenario_skill_match.json"),
        utilization_weight=20.0,    # Niedrigere Gewichtung für Auslastung
        skill_match_weight=60.0,    # Hohe Gewichtung für Skill-Match
        priority_weight=15.0,
        preference_weight=5.0
    )


def scenario_respect_preferences():
    """Szenario: Respektiere Präferenzen und Prioritäten"""
    print("\n" + "=" * 80)
    print("SZENARIO 3: Präferenzen & Prioritäten")
    print("=" * 80)

    run_optimization(
        employees_file=str(project_root / "data" / "employees.json"),
        projects_file=str(project_root / "data" / "projects.json"),
        constraints_file=str(project_root / "data" / "constraints.json"),
        output_file=str(project_root / "output" / "scenario_preferences.json"),
        utilization_weight=30.0,
        skill_match_weight=30.0,
        priority_weight=25.0,       # Höhere Gewichtung für Projekt-Priorität
        preference_weight=15.0      # Höhere Gewichtung für Präferenzen
    )


if __name__ == "__main__":
    print("Resource Allocation Optimizer - Verschiedene Szenarien")

    scenario_maximize_utilization()
    scenario_perfect_skill_match()
    scenario_respect_preferences()

    print("\n✅ Alle Szenarien erfolgreich durchgeführt!")
    print("   Ergebnisse wurden im output/ Verzeichnis gespeichert.")
