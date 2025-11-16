# 📊 Beispieldaten für Resource Allocation Optimizer

Dieses Verzeichnis enthält verschiedene Beispiel-Szenarien, die Sie zum Testen und Verstehen des Systems nutzen können.

## 📁 Verfügbare Szenarien

### 1. 🎓 Tutorial (`tutorial/`)

**Zweck:** Einfaches Einstiegs-Beispiel zum Kennenlernen des Systems

**Umfang:**
- 3 Mitarbeitende
- 3 Projekte
- 1 Constraint

**Charakteristika:**
- Einfache, klare Zuordnungen
- Mix aus Vollzeit (100%) und Teilzeit (50%)
- Alle Senioritätsstufen vertreten
- Perfekte Skill-Matches möglich

**Verwendung:**
```bash
python examples/run_tutorial.py
```

**Erwartetes Ergebnis:**
- ~95-100% Mitarbeiter-Auslastung
- ~100% Projekt-Abdeckung
- Alle Projekte sollten besetzt werden können

---

### 2. 🏢 Enterprise (`enterprise/`)

**Zweck:** Realistisches Szenario eines mittleren bis großen Unternehmens

**Umfang:**
- 20 Mitarbeitende
- 15 Projekte
- 15 Constraints

**Charakteristika:**
- Diverse Skills (ML, Cloud, Mobile, Security, etc.)
- Verschiedene Senioritätsstufen (Junior bis Principal)
- Realistische Teilzeit-Quoten (30%-100%)
- Komplexe Projekt-Anforderungen
- Viele bevorzugte und ausgeschlossene Zuordnungen

**Highlights:**
- KI-Projekte mit hohen Seniority-Anforderungen
- Cloud-Migration mit spezialisierten Skills
- Security-Audit mit dediziertem Experten
- Blockchain-Integration
- Product Management

**Verwendung:**
```bash
python examples/run_enterprise.py
```

**Erwartetes Ergebnis:**
- ~85-95% Mitarbeiter-Auslastung
- ~90-100% Projekt-Abdeckung
- Einige Projekte könnten unterbesetzt sein

---

### 3. ⚠️ Challenging (`challenging/`)

**Zweck:** Schwieriges Szenario mit vielen Herausforderungen und Constraints

**Umfang:**
- 8 Mitarbeitende
- 9 Projekte
- 7 Constraints

**Charakteristika:**
- **Extreme Teilzeit-Quoten:** Viele Mitarbeitende nur 30-60% verfügbar
- **Skill-Mismatches:** Nicht alle Projekte haben passende Experten
- **Hohe Seniority-Anforderungen:** Viele Projekte brauchen Seniors, aber wenig Senior-Kapazität
- **Überbuchung:** Mehr Projekt-Bedarf als verfügbare Kapazität
- **Spezialisierte Skills:** Nur einzelne Personen mit bestimmten Fähigkeiten

**Spezielle Herausforderungen:**
- Projekt benötigt ML + Senior, aber nur Junior verfügbar
- Legacy-Projekt braucht Experten der nur 30% verfügbar ist
- DevOps-Projekt braucht Kubernetes-Skills die niemand hat
- Mobile-Projekt ohne passende Mobile-Developer

**Verwendung:**
```bash
python examples/run_challenging.py
```

**Erwartetes Ergebnis:**
- ~60-80% Mitarbeiter-Auslastung
- ~70-90% Projekt-Abdeckung
- Mehrere unterbesetzte Projekte
- Zeigt wie der Optimizer mit Unmöglichem umgeht

---

## 🎯 Welches Szenario soll ich wählen?

| Szenario | Wenn Sie... | Lernen Sie... |
|----------|------------|---------------|
| **Tutorial** | Das System kennenlernen möchten | Grundlegende Funktionsweise |
| **Enterprise** | Ein realistisches Setup testen wollen | Komplexe Zuordnungen, viele Constraints |
| **Challenging** | Grenzen des Systems testen möchten | Umgang mit unmöglichen Anforderungen |

---

## 📖 Struktur der JSON-Dateien

### `employees.json`

```json
[
  {
    "id": "emp001",                    // Eindeutige ID (Pflicht)
    "name": "Anna Müller",             // Name (Pflicht)
    "skills": ["Python", "ML"],        // Skills (Pflicht, min. 1)
    "seniority": "senior",             // junior|intermediate|senior|lead|principal
    "availability": 1.0,               // 0.0-1.0 (1.0 = Vollzeit)
    "hourly_cost": 85                  // Optional: Stundensatz
  }
]
```

### `projects.json`

```json
[
  {
    "id": "proj001",                   // Eindeutige ID (Pflicht)
    "name": "KI-Chatbot",              // Name (Pflicht)
    "required_skills": ["Python"],     // Benötigte Skills (Pflicht)
    "min_seniority": "intermediate",   // Minimale Seniority
    "required_capacity": 1.5,          // Benötigte FTE
    "max_team_size": 3,                // Optional: Max. Personen
    "priority": 9                      // 1-10 (höher = wichtiger)
  }
]
```

### `constraints.json`

```json
[
  {
    "employee_id": "emp001",           // Mitarbeiter-ID
    "project_id": "proj001",           // Projekt-ID
    "type": "preferred",               // "preferred" oder "excluded"
    "weight": 2.0                      // Nur bei "preferred"
  }
]
```

---

## 🔧 Eigene Beispieldaten erstellen

1. **Kopieren Sie ein bestehendes Szenario:**
   ```bash
   cp -r data/tutorial data/my_scenario
   ```

2. **Bearbeiten Sie die JSON-Dateien** nach Ihren Bedürfnissen

3. **Validierung:**
   - Stellen Sie sicher, dass alle IDs eindeutig sind
   - Skills müssen übereinstimmen (case-sensitive!)
   - `availability` muss zwischen 0.0 und 1.0 liegen
   - `priority` zwischen 1 und 10

4. **Ausführen:**
   ```python
   from src.main import run_optimization

   summary = run_optimization(
       employees_file="data/my_scenario/employees.json",
       projects_file="data/my_scenario/projects.json",
       constraints_file="data/my_scenario/constraints.json"
   )
   ```

---

## 💡 Tipps für realistische Daten

### Skills definieren
- **Zu spezifisch:** `["React 18.2", "TypeScript 5.0"]` ❌
- **Zu generisch:** `["Programming"]` ❌
- **Gut:** `["React", "TypeScript", "JavaScript"]` ✅

### Seniority-Levels
- **Junior:** 0-2 Jahre Erfahrung
- **Intermediate:** 2-5 Jahre
- **Senior:** 5-10 Jahre
- **Lead:** 10+ Jahre + Führung
- **Principal:** Top-Experte, Architekt-Level

### Availability
- **1.0:** Vollzeit (40h/Woche)
- **0.8:** 32h/Woche (z.B. 4-Tage-Woche)
- **0.5:** Halbtags (20h/Woche)
- **0.3:** Beratende Rolle, nur wenige Stunden

### Projekt-Kapazität
- **1.0:** Eine Vollzeitkraft
- **1.5:** 1.5 Vollzeitkräfte (z.B. ein Senior + ein Junior)
- **0.5:** Halbes Team (z.B. für kleine Projekte)

---

## 🚀 Alle Szenarien auf einmal ausführen

```bash
python examples/run_all_scenarios.py
```

Dies führt nacheinander alle drei Szenarien aus und zeigt die Unterschiede.

---

## 📊 Ergebnisse interpretieren

### Gute Ergebnisse
- **Auslastung > 85%:** Die meisten Mitarbeitenden sind eingeplant
- **Projekt-Coverage > 90%:** Die meisten Projekte sind gut besetzt
- **Wenig unassigned:** Kaum Mitarbeitende ohne Projekt

### Problematische Ergebnisse
- **Auslastung < 60%:** Viele Mitarbeitende haben keine passenden Projekte
- **Projekt-Coverage < 70%:** Viele Projekte können nicht besetzt werden
- **Viele underallocated:** Skill-Mismatch oder zu wenig Kapazität

### Lösungen bei Problemen
1. **Projekt-Prioritäten anpassen:** Unwichtige Projekte zurückstellen
2. **Skills erweitern:** Mitarbeitende weiterbilden
3. **Externe Ressourcen:** Freelancer oder Dienstleister einplanen
4. **Gewichtungen anpassen:** Mehr Fokus auf Projekt-Coverage
5. **Teilzeit aufstocken:** Verfügbarkeit erhöhen

---

## 🆘 Häufige Fehler

### "Skills müssen übereinstimmen"
❌ `employee: ["python"]` vs `project: ["Python"]`
✅ Groß-/Kleinschreibung muss identisch sein!

### "Keine validen Zuordnungen möglich"
- Prüfen Sie ob `min_seniority` nicht zu hoch ist
- Prüfen Sie ob Skills übereinstimmen
- Reduzieren Sie ausgeschlossene Constraints

### "Projekt-Coverage = 0%"
- Keine Mitarbeitenden mit passenden Skills
- Alle passenden Mitarbeitenden sind bereits voll ausgelastet
- Seniority-Anforderungen zu hoch

---

## 📞 Support

Bei Fragen zu den Beispieldaten:
1. Prüfen Sie die JSON-Syntax (z.B. mit jsonlint.com)
2. Validieren Sie die Datenmodelle (siehe `src/models.py`)
3. Schauen Sie sich die bestehenden Beispiele an
4. Erstellen Sie ein Issue im Repository
