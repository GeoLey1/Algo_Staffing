"""Resource Allocation Optimizer - Linear Programming Implementation"""

from typing import List, Dict, Tuple
import pulp
from .models import (
    Employee, Project, Constraint, AllocationResult,
    OptimizationSummary, SeniorityLevel
)


class ResourceAllocationOptimizer:
    """
    Optimiert die Zuordnung von Mitarbeitenden zu Projekten.

    Optimierungsziele:
    - Maximale Auslastung der Mitarbeitenden
    - Optimale Skill-Besetzung (höherer Skill-Match = besser)
    - Berücksichtigung von Projekt-Prioritäten
    - Bevorzugte Zuordnungen fördern
    """

    # Seniority-Level Mapping für Vergleiche
    SENIORITY_RANK = {
        SeniorityLevel.JUNIOR: 1,
        SeniorityLevel.INTERMEDIATE: 2,
        SeniorityLevel.SENIOR: 3,
        SeniorityLevel.LEAD: 4,
        SeniorityLevel.PRINCIPAL: 5
    }

    def __init__(
        self,
        employees: List[Employee],
        projects: List[Project],
        constraints: List[Constraint] = None,
        utilization_weight: float = 40.0,
        skill_match_weight: float = 40.0,
        priority_weight: float = 15.0,
        preference_weight: float = 5.0
    ):
        """
        Initialisiert den Optimizer.

        Args:
            employees: Liste der Mitarbeitenden
            projects: Liste der Projekte
            constraints: Liste der Constraints (bevorzugt/ausgeschlossen)
            utilization_weight: Gewichtung für Auslastungs-Optimierung
            skill_match_weight: Gewichtung für Skill-Match-Optimierung
            priority_weight: Gewichtung für Projekt-Prioritäten
            preference_weight: Gewichtung für bevorzugte Zuordnungen
        """
        self.employees = {e.id: e for e in employees}
        self.projects = {p.id: p for p in projects}
        self.constraints = constraints or []

        # Gewichtungen normalisieren
        total_weight = (utilization_weight + skill_match_weight +
                       priority_weight + preference_weight)
        self.utilization_weight = utilization_weight / total_weight
        self.skill_match_weight = skill_match_weight / total_weight
        self.priority_weight = priority_weight / total_weight
        self.preference_weight = preference_weight / total_weight

        # Constraints parsen
        self._parse_constraints()

    def _parse_constraints(self):
        """Parst die Constraints in bevorzugte und ausgeschlossene Sets"""
        self.excluded = set()
        self.preferred = {}

        for constraint in self.constraints:
            key = (constraint.employee_id, constraint.project_id)
            if constraint.type == 'excluded':
                self.excluded.add(key)
            elif constraint.type == 'preferred':
                self.preferred[key] = constraint.weight

    def _calculate_skill_match_score(self, employee: Employee, project: Project) -> float:
        """
        Berechnet Skill-Match Score zwischen Mitarbeitendem und Projekt.

        Returns:
            Score zwischen 0.0 (kein Match) und 1.0 (perfekter Match)
        """
        employee_skills = set(employee.skills)
        required_skills = set(project.required_skills)

        # Keine Skills erfüllt = 0
        if not employee_skills.intersection(required_skills):
            return 0.0

        # Anteil der erfüllten Skills
        match_ratio = len(employee_skills.intersection(required_skills)) / len(required_skills)

        # Bonus für zusätzliche relevante Skills
        extra_skills_bonus = min(0.1, len(employee_skills - required_skills) * 0.02)

        # Seniority-Bonus (Senior auf Junior-Projekt = kleiner Bonus, umgekehrt = Malus)
        emp_rank = self.SENIORITY_RANK[employee.seniority]
        proj_rank = self.SENIORITY_RANK[project.min_seniority]
        seniority_factor = 1.0
        if emp_rank >= proj_rank:
            seniority_factor = 1.0 + (emp_rank - proj_rank) * 0.05  # Bonus für höhere Seniority
        else:
            seniority_factor = 0.5  # Malus wenn Seniority zu niedrig

        return min(1.0, match_ratio * seniority_factor + extra_skills_bonus)

    def _is_valid_assignment(self, employee: Employee, project: Project) -> bool:
        """
        Prüft ob eine Zuordnung grundsätzlich möglich ist.

        Bedingungen:
        - Mindestens ein Skill-Match
        - Seniority ausreichend
        - Nicht in excluded Constraints
        """
        # Excluded check
        if (employee.id, project.id) in self.excluded:
            return False

        # Skill check - mindestens ein Match erforderlich
        if not set(employee.skills).intersection(set(project.required_skills)):
            return False

        # Seniority check
        emp_rank = self.SENIORITY_RANK[employee.seniority]
        proj_rank = self.SENIORITY_RANK[project.min_seniority]
        if emp_rank < proj_rank:
            return False

        return True

    def optimize(self) -> OptimizationSummary:
        """
        Führt die Optimierung durch.

        Returns:
            OptimizationSummary mit den Ergebnissen
        """
        # Problem definieren (Maximierung)
        prob = pulp.LpProblem("Resource_Allocation", pulp.LpMaximize)

        # Entscheidungsvariablen: x[e,p] = Kapazität von Employee e auf Projekt p
        # (kontinuierlich zwischen 0 und employee.availability)
        x = {}
        for emp_id, employee in self.employees.items():
            for proj_id, project in self.projects.items():
                if self._is_valid_assignment(employee, project):
                    x[emp_id, proj_id] = pulp.LpVariable(
                        f"x_{emp_id}_{proj_id}",
                        lowBound=0,
                        upBound=employee.availability,
                        cat='Continuous'
                    )

        # Hilfsvariablen für Projektabdeckung
        project_coverage = {}
        for proj_id in self.projects:
            project_coverage[proj_id] = pulp.LpVariable(
                f"coverage_{proj_id}",
                lowBound=0,
                upBound=1,
                cat='Continuous'
            )

        # Zielfunktion: Gewichtete Summe aus verschiedenen Zielen
        objective_terms = []

        # 1. Auslastung: Maximiere genutzte Kapazität
        total_available_capacity = sum(e.availability for e in self.employees.values())
        if total_available_capacity > 0:
            utilization_term = (
                pulp.lpSum([x[emp_id, proj_id] for (emp_id, proj_id) in x]) /
                total_available_capacity
            )
            objective_terms.append(self.utilization_weight * utilization_term)

        # 2. Skill-Match: Maximiere Skill-Match-Quality
        skill_match_term = pulp.lpSum([
            self._calculate_skill_match_score(
                self.employees[emp_id],
                self.projects[proj_id]
            ) * x[emp_id, proj_id]
            for (emp_id, proj_id) in x
        ])
        if len(x) > 0:
            objective_terms.append(self.skill_match_weight * skill_match_term / len(x))

        # 3. Projekt-Priorität: Bevorzuge wichtige Projekte
        priority_term = pulp.lpSum([
            (self.projects[proj_id].priority / 10.0) * project_coverage[proj_id]
            for proj_id in self.projects
        ])
        if len(self.projects) > 0:
            objective_terms.append(self.priority_weight * priority_term / len(self.projects))

        # 4. Bevorzugte Zuordnungen
        if self.preferred:
            preference_term = pulp.lpSum([
                self.preferred.get((emp_id, proj_id), 0) * x[emp_id, proj_id]
                for (emp_id, proj_id) in x
                if (emp_id, proj_id) in self.preferred
            ])
            objective_terms.append(self.preference_weight * preference_term / len(self.preferred))

        prob += pulp.lpSum(objective_terms), "Weighted_Objective"

        # Constraints

        # C1: Mitarbeiter-Kapazität darf nicht überschritten werden
        for emp_id, employee in self.employees.items():
            relevant_vars = [x[emp_id, proj_id] for proj_id in self.projects
                           if (emp_id, proj_id) in x]
            if relevant_vars:
                prob += (
                    pulp.lpSum(relevant_vars) <= employee.availability,
                    f"Capacity_{emp_id}"
                )

        # C2: Projekt-Coverage Definition
        for proj_id, project in self.projects.items():
            relevant_vars = [x[emp_id, proj_id] for emp_id in self.employees
                           if (emp_id, proj_id) in x]
            if relevant_vars and project.required_capacity > 0:
                prob += (
                    project_coverage[proj_id] <= pulp.lpSum(relevant_vars) / project.required_capacity,
                    f"Coverage_def_{proj_id}"
                )
                prob += (
                    project_coverage[proj_id] <= 1.0,
                    f"Coverage_max_{proj_id}"
                )

        # C3: Max Team Size (optional)
        for proj_id, project in self.projects.items():
            if project.max_team_size is not None:
                # Binärvariablen: ist Employee auf Projekt zugeordnet?
                y = {}
                for emp_id in self.employees:
                    if (emp_id, proj_id) in x:
                        y[emp_id] = pulp.LpVariable(
                            f"assigned_{emp_id}_{proj_id}",
                            cat='Binary'
                        )
                        # y[emp_id] = 1 wenn x[emp_id, proj_id] > 0
                        prob += x[emp_id, proj_id] <= employee.availability * y[emp_id]

                if y:
                    prob += (
                        pulp.lpSum(y.values()) <= project.max_team_size,
                        f"MaxTeamSize_{proj_id}"
                    )

        # Optimierung durchführen
        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        # Ergebnisse sammeln
        allocations = []
        employee_utilization = {emp_id: 0.0 for emp_id in self.employees}
        project_allocated = {proj_id: 0.0 for proj_id in self.projects}

        for (emp_id, proj_id), var in x.items():
            allocated = var.varValue
            if allocated and allocated > 0.001:  # Mindest-Threshold
                employee = self.employees[emp_id]
                project = self.projects[proj_id]

                allocations.append(AllocationResult(
                    employee_id=emp_id,
                    employee_name=employee.name,
                    project_id=proj_id,
                    project_name=project.name,
                    allocated_capacity=round(allocated, 3),
                    skill_match_score=round(
                        self._calculate_skill_match_score(employee, project), 3
                    ),
                    is_preferred=(emp_id, proj_id) in self.preferred
                ))

                employee_utilization[emp_id] += allocated
                project_allocated[proj_id] += allocated

        # Zusammenfassung berechnen
        total_available = sum(e.availability for e in self.employees.values())
        total_utilized = sum(employee_utilization.values())
        total_employee_utilization = (
            (total_utilized / total_available * 100) if total_available > 0 else 0
        )

        total_required = sum(p.required_capacity for p in self.projects.values())
        total_project_allocated = sum(project_allocated.values())
        total_project_coverage = (
            (total_project_allocated / total_required * 100) if total_required > 0 else 0
        )

        unassigned = [
            emp_id for emp_id, util in employee_utilization.items()
            if util < 0.001
        ]

        underallocated = [
            proj_id for proj_id, allocated in project_allocated.items()
            if allocated < self.projects[proj_id].required_capacity * 0.9  # <90% abgedeckt
        ]

        return OptimizationSummary(
            total_allocations=len(allocations),
            total_employee_utilization=round(total_employee_utilization, 2),
            total_project_coverage=round(total_project_coverage, 2),
            unassigned_employees=unassigned,
            underallocated_projects=underallocated,
            objective_value=round(pulp.value(prob.objective), 4) if prob.objective else 0,
            allocations=sorted(allocations, key=lambda a: (a.project_id, -a.allocated_capacity))
        )
