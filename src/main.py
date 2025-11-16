"""Resource Allocation Optimizer - Hauptprogramm"""

import json
from pathlib import Path
from typing import List, Dict
from .models import Employee, Project, Constraint, OptimizationSummary
from .optimizer import ResourceAllocationOptimizer


def load_employees(file_path: str) -> List[Employee]:
    """Lädt Mitarbeitende aus JSON-Datei"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Employee(**emp) for emp in data]


def load_projects(file_path: str) -> List[Project]:
    """Lädt Projekte aus JSON-Datei"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Project(**proj) for proj in data]


def load_constraints(file_path: str) -> List[Constraint]:
    """Lädt Constraints aus JSON-Datei"""
    if not Path(file_path).exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Constraint(**constraint) for constraint in data]


def print_summary(summary: OptimizationSummary):
    """Gibt Optimierungs-Ergebnis formatiert aus"""
    print("\n" + "="*80)
    print("RESOURCE ALLOCATION OPTIMIZATION - ERGEBNISSE")
    print("="*80)

    print(f"\nGesamtanzahl Zuordnungen: {summary.total_allocations}")
    print(f"Mitarbeiter-Auslastung: {summary.total_employee_utilization:.1f}%")
    print(f"Projekt-Abdeckung: {summary.total_project_coverage:.1f}%")
    print(f"Objective Value: {summary.objective_value:.4f}")

    if summary.unassigned_employees:
        print(f"\nNicht zugeordnete Mitarbeitende ({len(summary.unassigned_employees)}):")
        for emp_id in summary.unassigned_employees:
            print(f"  - {emp_id}")

    if summary.underallocated_projects:
        print(f"\nUnterbesetzte Projekte ({len(summary.underallocated_projects)}):")
        for proj_id in summary.underallocated_projects:
            print(f"  - {proj_id}")

    print("\n" + "-"*80)
    print("ZUORDNUNGEN")
    print("-"*80)

    current_project = None
    for allocation in summary.allocations:
        if allocation.project_id != current_project:
            current_project = allocation.project_id
            print(f"\n📋 Projekt: {allocation.project_name} ({allocation.project_id})")

        preferred_marker = " ⭐" if allocation.is_preferred else ""
        print(f"  → {allocation.employee_name:20} | "
              f"Kapazität: {allocation.allocated_capacity:4.1%} | "
              f"Skill-Match: {allocation.skill_match_score:4.1%}{preferred_marker}")

    print("\n" + "="*80 + "\n")


def save_results(summary: OptimizationSummary, output_file: str):
    """Speichert Ergebnisse als JSON"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary.model_dump(), f, indent=2, ensure_ascii=False)
    print(f"Ergebnisse gespeichert in: {output_file}")


def run_optimization(
    employees_file: str = "data/employees.json",
    projects_file: str = "data/projects.json",
    constraints_file: str = "data/constraints.json",
    output_file: str = "output/allocation_results.json",
    utilization_weight: float = 40.0,
    skill_match_weight: float = 40.0,
    priority_weight: float = 15.0,
    preference_weight: float = 5.0
) -> OptimizationSummary:
    """
    Führt vollständige Optimierung durch.

    Args:
        employees_file: Pfad zur Mitarbeiter-Datei
        projects_file: Pfad zur Projekt-Datei
        constraints_file: Pfad zur Constraints-Datei
        output_file: Pfad für Ergebnis-Datei
        utilization_weight: Gewichtung Auslastung (Standard: 40%)
        skill_match_weight: Gewichtung Skill-Match (Standard: 40%)
        priority_weight: Gewichtung Projekt-Priorität (Standard: 15%)
        preference_weight: Gewichtung Präferenzen (Standard: 5%)

    Returns:
        OptimizationSummary mit Ergebnissen
    """
    print("Lade Daten...")
    employees = load_employees(employees_file)
    projects = load_projects(projects_file)
    constraints = load_constraints(constraints_file)

    print(f"  {len(employees)} Mitarbeitende geladen")
    print(f"  {len(projects)} Projekte geladen")
    print(f"  {len(constraints)} Constraints geladen")

    print("\nStarte Optimierung...")
    optimizer = ResourceAllocationOptimizer(
        employees=employees,
        projects=projects,
        constraints=constraints,
        utilization_weight=utilization_weight,
        skill_match_weight=skill_match_weight,
        priority_weight=priority_weight,
        preference_weight=preference_weight
    )

    summary = optimizer.optimize()

    print_summary(summary)

    # Ausgabeverzeichnis erstellen falls nicht vorhanden
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    save_results(summary, output_file)

    return summary


if __name__ == "__main__":
    # Beispielaufruf mit Standardwerten
    run_optimization()
