# 🚀 Beispiele für Resource Allocation Optimizer

Dieses Verzeichnis enthält verschiedene Beispiel-Scripts, die Sie ausführen können.

## 📖 Verfügbare Beispiele

### 1️⃣ Einfaches Beispiel (`simple_example.py`)

Das Standard-Beispiel mit den Daten aus `data/` (10 Mitarbeitende, 7 Projekte).

```bash
python examples/simple_example.py
```

**Zeigt:**
- Grundlegende Verwendung der Optimierung
- Standard-Gewichtungen (40% Auslastung, 40% Skill-Match, 15% Priorität, 5% Präferenzen)
- Formatierte Ausgabe der Ergebnisse

---

### 2️⃣ Tutorial-Szenario (`run_tutorial.py`)

Kleines, einfaches Beispiel zum Kennenlernen (3 Mitarbeitende, 3 Projekte).

```bash
python examples/run_tutorial.py
```

**Erwartetes Ergebnis:**
- ✅ 100% Mitarbeiter-Auslastung
- ✅ ~100% Projekt-Abdeckung
- ✅ Perfekte Zuordnungen

**Ideal für:**
- Erste Schritte mit dem System
- Verstehen der grundlegenden Konzepte
- Testen von Änderungen

---

### 3️⃣ Enterprise-Szenario (`run_enterprise.py`)

Realistisches großes Unternehmen (20 Mitarbeitende, 15 Projekte).

```bash
python examples/run_enterprise.py
```

**Erwartetes Ergebnis:**
- ⚠️ ~84% Mitarbeiter-Auslastung
- ⚠️ ~84% Projekt-Abdeckung
- ⚠️ Einige unterbesetzte Projekte

**Zeigt:**
- Komplexe Zuordnungen mit vielen Constraints
- Realistische Skill-Verteilung
- Umgang mit verschiedenen Senioritätsstufen
- Teilzeit-Management

---

### 4️⃣ Challenging-Szenario (`run_challenging.py`)

Schwieriges Szenario mit vielen Herausforderungen (8 Mitarbeitende, 9 Projekte).

```bash
python examples/run_challenging.py
```

**Erwartetes Ergebnis:**
- ⚠️ ~90% Mitarbeiter-Auslastung (aber viele ohne Projekt)
- ❌ ~50% Projekt-Abdeckung (viele Projekte unterbesetzt)
- ⚠️ Viele Warnungen

**Zeigt:**
- Umgang mit extremen Teilzeit-Quoten (30-80%)
- Skill-Mismatches (fehlende Experten)
- Überbuchung (mehr Bedarf als Kapazität)
- Wie der Optimizer priorisiert wenn nicht alles möglich ist

---

### 5️⃣ Angepasste Gewichtungen (`custom_weights_example.py`)

Zeigt verschiedene Optimierungs-Szenarien mit unterschiedlichen Gewichtungen.

```bash
python examples/custom_weights_example.py
```

**Führt aus:**
1. **Szenario 1:** Maximale Auslastung (70% Gewichtung)
2. **Szenario 2:** Perfekter Skill-Match (60% Gewichtung)
3. **Szenario 3:** Präferenzen & Prioritäten (höhere Gewichtung)

**Zeigt:**
- Wie Gewichtungen das Ergebnis beeinflussen
- Trade-offs zwischen verschiedenen Zielen
- Anpassung an verschiedene Geschäftsszenarien

---

### 6️⃣ Alle Szenarien (`run_all_scenarios.py`)

Führt alle drei Szenarien (Tutorial, Enterprise, Challenging) nacheinander aus.

```bash
python examples/run_all_scenarios.py
```

**Nützlich für:**
- Vergleich verschiedener Szenarien
- Demonstrations-Zwecke
- Testing nach Änderungen am Code

---

## 🎯 Welches Beispiel soll ich ausführen?

| Beispiel | Verwenden Sie wenn... |
|----------|----------------------|
| `simple_example.py` | Sie das System zum ersten Mal ausprobieren |
| `run_tutorial.py` | Sie die Grundlagen verstehen möchten |
| `run_enterprise.py` | Sie ein realistisches Setup testen wollen |
| `run_challenging.py` | Sie Grenzen des Systems testen möchten |
| `custom_weights_example.py` | Sie verschiedene Optimierungsziele vergleichen wollen |
| `run_all_scenarios.py` | Sie alle Szenarien auf einmal sehen möchten |

---

## 📊 Ausgabe verstehen

### Erfolgreich ✅

```
Mitarbeiter-Auslastung: 95.0%     ← Die meisten sind eingeplant
Projekt-Abdeckung: 98.0%          ← Fast alle Projekte besetzt
Gesamtanzahl Zuordnungen: 15      ← Viele erfolgreiche Matches
```

### Problematisch ⚠️

```
Mitarbeiter-Auslastung: 60.0%     ← Viele ohne Projekt
Projekt-Abdeckung: 65.0%          ← Viele Projekte unterbesetzt
Nicht zugeordnete Mitarbeitende (5)
Unterbesetzte Projekte (8)
```

**Was tun?**
1. Prüfen Sie `unassigned_employees` - warum passen deren Skills nicht?
2. Prüfen Sie `underallocated_projects` - fehlen passende Experten?
3. Passen Sie Gewichtungen an
4. Reduzieren Sie Projekt-Scope oder erweitern Sie das Team

---

## 🔧 Eigene Beispiele erstellen

### Kopiervorlage:

```python
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.main import run_optimization

summary = run_optimization(
    employees_file="data/meine_daten/employees.json",
    projects_file="data/meine_daten/projects.json",
    constraints_file="data/meine_daten/constraints.json",
    output_file="output/mein_ergebnis.json",
    utilization_weight=40.0,
    skill_match_weight=40.0,
    priority_weight=15.0,
    preference_weight=5.0
)

print(f"Ergebnis: {summary.total_employee_utilization:.1f}% Auslastung")
```

---

## 💡 Tipps

### Performance
- Kleine Szenarien (<10 Personen): <1 Sekunde
- Mittlere Szenarien (10-30 Personen): 1-5 Sekunden
- Große Szenarien (30-100 Personen): 5-30 Sekunden

### Debugging
Wenn ein Beispiel nicht funktioniert:
1. Prüfen Sie die JSON-Syntax (mit jsonlint.com)
2. Validieren Sie dass Skills exakt übereinstimmen (case-sensitive!)
3. Prüfen Sie dass alle referenzierten IDs existieren
4. Schauen Sie in die Fehlermeldung - Pydantic gibt hilfreiche Validierungs-Fehler

### Best Practices
- Starten Sie mit `simple_example.py`
- Testen Sie Ihre eigenen Daten zuerst mit wenigen Mitarbeitenden
- Erhöhen Sie schrittweise die Komplexität
- Nutzen Sie verschiedene Gewichtungen um Trade-offs zu verstehen

---

## 📖 Weitere Dokumentation

- **Beispieldaten:** Siehe `data/BEISPIELDATEN.md`
- **Hauptdokumentation:** Siehe `README.md` im Root-Verzeichnis
- **Code-Dokumentation:** Siehe Docstrings in `src/`

---

## 🆘 Support

Bei Problemen:
1. Prüfen Sie die Beispiel-Ausgaben oben
2. Validieren Sie Ihre JSON-Dateien
3. Lesen Sie `data/BEISPIELDATEN.md` für Datenformat
4. Erstellen Sie ein Issue mit Ihrem Szenario (anonymisiert)
