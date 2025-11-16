"""Datenmodelle für Resource Allocation Optimizer"""

from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class SeniorityLevel(str, Enum):
    """Senioritätsstufen"""
    JUNIOR = "junior"
    INTERMEDIATE = "intermediate"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"


class Employee(BaseModel):
    """Mitarbeiter-Modell"""
    id: str = Field(..., description="Eindeutige Mitarbeiter-ID")
    name: str = Field(..., description="Name des Mitarbeitenden")
    skills: List[str] = Field(..., description="Liste der Skills/Qualifikationen")
    seniority: SeniorityLevel = Field(..., description="Senioritätsstufe")
    availability: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Verfügbarkeit (0.0-1.0, z.B. 0.5 für 50% Teilzeit)"
    )
    hourly_cost: Optional[float] = Field(
        default=None,
        description="Stundensatz für Kostenoptimierung (optional)"
    )

    @field_validator('skills')
    @classmethod
    def skills_not_empty(cls, v):
        if not v:
            raise ValueError('Mitarbeitende müssen mindestens einen Skill haben')
        return v


class Project(BaseModel):
    """Projekt-Modell"""
    id: str = Field(..., description="Eindeutige Projekt-ID")
    name: str = Field(..., description="Projektname")
    required_skills: List[str] = Field(..., description="Benötigte Skills")
    min_seniority: SeniorityLevel = Field(
        default=SeniorityLevel.JUNIOR,
        description="Minimale Senioritätsstufe"
    )
    required_capacity: float = Field(
        default=1.0,
        ge=0.0,
        description="Benötigte Kapazität (1.0 = eine Vollzeitkraft)"
    )
    max_team_size: Optional[int] = Field(
        default=None,
        description="Maximale Team-Größe (optional)"
    )
    priority: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Projekt-Priorität (1-10, höher = wichtiger)"
    )

    @field_validator('required_skills')
    @classmethod
    def required_skills_not_empty(cls, v):
        if not v:
            raise ValueError('Projekte müssen mindestens einen benötigten Skill haben')
        return v


class Constraint(BaseModel):
    """Zuordnungs-Constraints"""
    employee_id: str = Field(..., description="Mitarbeiter-ID")
    project_id: str = Field(..., description="Projekt-ID")
    type: str = Field(..., description="Constraint-Typ: 'preferred' oder 'excluded'")
    weight: float = Field(
        default=1.0,
        ge=0.0,
        description="Gewichtung für bevorzugte Zuordnungen (nur bei 'preferred')"
    )

    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        if v not in ['preferred', 'excluded']:
            raise ValueError("type muss 'preferred' oder 'excluded' sein")
        return v


class AllocationResult(BaseModel):
    """Ergebnis der Optimierung"""
    employee_id: str
    employee_name: str
    project_id: str
    project_name: str
    allocated_capacity: float
    skill_match_score: float
    is_preferred: bool


class OptimizationSummary(BaseModel):
    """Zusammenfassung der Optimierung"""
    total_allocations: int
    total_employee_utilization: float
    total_project_coverage: float
    unassigned_employees: List[str]
    underallocated_projects: List[str]
    objective_value: float
    allocations: List[AllocationResult]
