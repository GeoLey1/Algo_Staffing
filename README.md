# Resource Allocation Optimizer

Ein intelligentes System zur optimalen Zuordnung von Mitarbeitenden zu Projekten mittels Linear Programming.

## 🎯 Features

- **Multi-Objective Optimierung**: Gleichzeitige Optimierung von:
  - Maximale Mitarbeiter-Auslastung
  - Optimaler Skill-Match zwischen Mitarbeitenden und Projekten
  - Berücksichtigung von Projekt-Prioritäten
  - Respektierung von Präferenzen

- **Flexible Constraints**:
  - Skills und Qualifikationen
  - Senioritätsstufen (Junior, Intermediate, Senior, Lead, Principal)
  - Teilzeit-Verfügbarkeit (z.B. 50%, 80%)
  - Bevorzugte Zuordnungen
  - Ausgeschlossene Zuordnungen
  - Max. Team-Größe pro Projekt

- **Anpassbare Gewichtungen**: Passen Sie die Optimierungsziele an Ihre Bedürfnisse an

## 📋 Anforderungen

- Python 3.8+
- PuLP (Linear Programming Solver)
- Pandas
- Pydantic

## 🚀 Installation

```bash
# Repository klonen
git clone <repository-url>
cd Algo_Staffing

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt
```

## 📖 Verwendung

### Schnellstart

```bash
# Einfaches Beispiel ausführen
python examples/simple_example.py
```

### Eigene Daten verwenden

1. **Mitarbeitende definieren** (`data/employees.json`):

```json
[
  {
    "id": "emp001",
    "name": "Anna Müller",
    "skills": ["Python", "Machine Learning", "Data Analysis"],
    "seniority": "senior",
    "availability": 1.0,
    "hourly_cost": 85
  },
  {
    "id": "emp002",
    "name": "Ben Schmidt",
    "skills": ["JavaScript", "React"],
    "seniority": "intermediate",
    "availability": 0.5
  }
]
```

**Felder**:
- `id`: Eindeutige Mitarbeiter-ID (Pflicht)
- `name`: Name (Pflicht)
- `skills`: Liste der Skills (Pflicht)
- `seniority`: junior|intermediate|senior|lead|principal (Pflicht)
- `availability`: 0.0-1.0 (Standard: 1.0 = Vollzeit)
- `hourly_cost`: Stundensatz (Optional)

2. **Projekte definieren** (`data/projects.json`):

```json
[
  {
    "id": "proj001",
    "name": "KI-Chatbot Entwicklung",
    "required_skills": ["Python", "Machine Learning"],
    "min_seniority": "intermediate",
    "required_capacity": 1.5,
    "max_team_size": 3,
    "priority": 9
  }
]
```

**Felder**:
- `id`: Eindeutige Projekt-ID (Pflicht)
- `name`: Projektname (Pflicht)
- `required_skills`: Benötigte Skills (Pflicht)
- `min_seniority`: Minimale Senioritätsstufe (Standard: junior)
- `required_capacity`: Benötigte Kapazität in FTE (Standard: 1.0)
- `max_team_size`: Max. Anzahl Personen (Optional)
- `priority`: 1-10, höher = wichtiger (Standard: 1)

3. **Constraints definieren** (`data/constraints.json`):

```json
[
  {
    "employee_id": "emp001",
    "project_id": "proj001",
    "type": "preferred",
    "weight": 2.0
  },
  {
    "employee_id": "emp002",
    "project_id": "proj005",
    "type": "excluded"
  }
]
```

**Typen**:
- `preferred`: Bevorzugte Zuordnung (mit optionaler Gewichtung)
- `excluded`: Ausgeschlossene Zuordnung (hard constraint)

### Programmatische Nutzung

```python
from src.main import run_optimization

# Standard-Optimierung
summary = run_optimization(
    employees_file="data/employees.json",
    projects_file="data/projects.json",
    constraints_file="data/constraints.json",
    output_file="output/results.json"
)

# Mit angepassten Gewichtungen
summary = run_optimization(
    employees_file="data/employees.json",
    projects_file="data/projects.json",
    constraints_file="data/constraints.json",
    output_file="output/results.json",
    utilization_weight=70.0,    # 70% Fokus auf Auslastung
    skill_match_weight=20.0,    # 20% Fokus auf Skill-Match
    priority_weight=8.0,        # 8% Fokus auf Prioritäten
    preference_weight=2.0       # 2% Fokus auf Präferenzen
)

# Ergebnisse analysieren
print(f"Auslastung: {summary.total_employee_utilization:.1f}%")
print(f"Projekt-Abdeckung: {summary.total_project_coverage:.1f}%")
print(f"Zuordnungen: {summary.total_allocations}")
```

## 🎛️ Gewichtungen anpassen

Die Optimierung verwendet vier Gewichtungen (Summe = 100%):

1. **utilization_weight** (Standard: 40%)
   - Maximiert die Auslastung der Mitarbeitenden
   - Höher setzen: Mehr Fokus auf volle Auslastung

2. **skill_match_weight** (Standard: 40%)
   - Maximiert die Qualität des Skill-Matches
   - Höher setzen: Perfekte Skill-Besetzung wichtiger als Auslastung

3. **priority_weight** (Standard: 15%)
   - Berücksichtigt Projekt-Prioritäten
   - Höher setzen: Wichtige Projekte werden bevorzugt besetzt

4. **preference_weight** (Standard: 5%)
   - Respektiert bevorzugte Zuordnungen
   - Höher setzen: Team-Präferenzen werden stärker berücksichtigt

### Beispiel-Szenarien

Siehe `examples/custom_weights_example.py` für verschiedene Optimierungsszenarien.

## 📊 Output

Die Optimierung liefert:

```json
{
  "total_allocations": 12,
  "total_employee_utilization": 87.5,
  "total_project_coverage": 95.2,
  "unassigned_employees": [],
  "underallocated_projects": ["proj007"],
  "objective_value": 0.8543,
  "allocations": [
    {
      "employee_id": "emp001",
      "employee_name": "Anna Müller",
      "project_id": "proj001",
      "project_name": "KI-Chatbot Entwicklung",
      "allocated_capacity": 1.0,
      "skill_match_score": 0.95,
      "is_preferred": true
    }
  ]
}
```

## 🔧 Algorithmus-Details

Der Optimizer verwendet **Linear Programming** (via PuLP):

- **Entscheidungsvariablen**: Kontinuierliche Variablen für die zugeordnete Kapazität jedes Mitarbeitenden auf jedem Projekt
- **Constraints**:
  - Mitarbeiter-Kapazität darf nicht überschritten werden
  - Nur valide Zuordnungen (Skill-Match + Seniority)
  - Ausgeschlossene Zuordnungen werden verboten
  - Optional: Max. Team-Größe pro Projekt
- **Objective**: Gewichtete Summe aus Auslastung, Skill-Match, Prioritäten und Präferenzen

### Skill-Match-Berechnung

Der Skill-Match-Score berücksichtigt:
1. Anteil der erfüllten required_skills (Haupt-Faktor)
2. Bonus für zusätzliche relevante Skills
3. Seniority-Bonus: Höhere Seniority als benötigt = Bonus
4. Seniority-Malus: Zu niedrige Seniority = nicht erlaubt

## 📁 Projektstruktur

```
Algo_Staffing/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── models.py           # Datenmodelle (Pydantic)
│   ├── optimizer.py        # Optimierungs-Algorithmus
│   └── main.py            # Hauptprogramm
├── data/
│   ├── employees.json     # Beispiel-Mitarbeitende
│   ├── projects.json      # Beispiel-Projekte
│   └── constraints.json   # Beispiel-Constraints
├── examples/
│   ├── simple_example.py
│   └── custom_weights_example.py
└── output/                # Ergebnisse (wird automatisch erstellt)
    └── *.json
```

## 🤝 Beitragen

Feedback und Beiträge sind willkommen! Erstellen Sie einfach ein Issue oder Pull Request.

## 📝 Lizenz

MIT License

## 🆘 Support

Bei Fragen oder Problemen:
1. Prüfen Sie die Beispiele in `examples/`
2. Validieren Sie Ihre JSON-Dateien
3. Erhöhen Sie die Gewichtungen schrittweise um das Verhalten zu verstehen
4. Erstellen Sie ein Issue mit Ihren Daten (anonymisiert)

## 🔄 Nächste Schritte

Mögliche Erweiterungen:
- Web-Interface (Streamlit/FastAPI)
- Excel-Import/Export
- Visualisierung der Zuordnungen
- Historische Analysen
- Cost-Optimierung
- Multi-Standort-Support
