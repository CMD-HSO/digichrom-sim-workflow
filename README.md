# DigiChrom: Simulation-Based Parameter Identification Workflow

[![Project: DigiChrom](https://img.shields.io/badge/Project-DigiChrom-blue.svg)](https://github.com/CMD-HSO/digichrom-sim-workflow)
[![Framework: MaterialDigital](https://img.shields.io/badge/Framework-MaterialDigital-green.svg)](https://material-digital.de/)
[![Language: Python 3](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)
[![FE Solver: Abaqus](https://img.shields.io/badge/FEA-Abaqus-red.svg)](https://www.3ds.com/products-services/simulia/products/abaqus/)

Automated workflow for identifying non-linear elasto-plastic constitutive material parameters (combined kinematic and isotropic hardening) of electroplated coatings based on instrumented indentation testing (nano/micro-indentation) and Finite Element Analysis (FEA).

Developed at **Offenburg University of Applied Sciences (HS Offenburg)** as part of the **DigiChrom** research initiative within the **MaterialDigital** platform.

---

## 📌 Overview

This repository provides an automated parameter identification framework that couples numerical optimization algorithms in **Python** with finite element simulations in **Dassault Systèmes Abaqus**. 

The workflow calibrates elasto-plastic constitutive models by minimizing the discrepancy between experimentally measured load-displacement curves (from instrumented indentation tests) and simulated responses.

### Key Features
- **Combined Hardening Calibration:** Identifies parameters for non-linear isotropic ($R_e, Q_{\infty}, b$) and kinematic ($C, \gamma$) hardening plasticity models.
- **Robust Optimization:** Utilizes Sequential Least Squares Programming (SLSQP via `scipy.optimize`) with initial parameter sampling (bounded Gaussian noise) to avoid local minima.
- **Abaqus FEA Coupling:** Fully automated generation of Abaqus keywords, job execution, and post-processing via Abaqus Python scripts.
- **Multi-Start Optimization:** Capability to launch multiple initial parameter sets to evaluate sensitivity and ensure optimization convergence.

---

## ⚙️ Workflow Architecture
                   ┌──────────────────────────────┐
                   │   Experimental Data (.txt)   │
                   │ (Time, Force, Displacement)  │
                   └──────────────┬───────────────┘
                                  │
                                  ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ Main Optimization Loop (Python / SLSQP)                                   │
│                                                                           │
│  1. Sample / Update Material Parameters (Re, Qinf, b, C, gamma)           │
│  2. Write Abaqus Include Files (indent_para.inp, indent_mat.inp, ...)     │
│  3. Execute FEA Solver (Abaqus Job Execution)                             │
│  4. Extract Reaction Forces & Displacements via Post-Processing Script    │
│  5. Compute Least-Squares Objective Function (Exp vs. Sim)                │
└──────────────────────────────┬────────────────────────────────────────────┘
                               │ Iterative Loop
                               ▼
┌──────────────────────────────┐
│  Optimized Parameter Set &   │
│    Fitted Curves (.out/.png) │
└──────────────────────────────┘

---

## 📁 Repository Structure

```text
├── Main_Optimization.py           # Main execution script (parameter setup & SLSQP loop)
├── DriveModel_Seifert.py          # Interface to handle Abaqus job submission & post-processing
├── ParameterStructure_Seifert.py  # Data class handling parameter bounds, scaling, and mapping
├── PlotResults_Seifert.py         # Utility module for plotting experimental vs. simulated curves
├── _postProc_IndPlast_Seifert.py  # Abaqus CAE GUI/noGUI post-processing script (node extraction)
├── indent_glob.inp                # Global Abaqus base template (mesh, boundary conditions)
├── data_indent.txt                # Sample experimental indentation data
└── README.md                      # Documentation


🚀 Requirements & InstallationPrerequisitesPython 3.x with the following packages:Bashpip install numpy scipy matplotlib
Dassault Systèmes Abaqus (must be executable via system command line abaqus).Running the WorkflowClone the repository:Bashgit clone [https://github.com/CMD-HSO/digichrom-sim-workflow.git](https://github.com/CMD-HSO/digichrom-sim-workflow.git)
cd digichrom-sim-workflow
Ensure your experimental data file (data_indent.txt) is formatted properly:Column 0: Time ($t$)Column 1: Measured Reaction Force ($F_{\text{exp}}$)Column 2: Controlled Displacement ($u_{\text{cntr}}$)Column 3: Temperature ($T$)Run the parameter identification workflow:Bashpython Main_Optimization.py
🔬 Constitutive Model ParametersThe optimization calibrates the following mechanical parameters for combined hardening:ParameterSymbolDescriptionE_________$E$Young's Modulusnue_______$\nu$Poisson's RatioRe________$\sigma_0$ / $R_e$Initial Yield StressQinf______$Q_{\infty}$Isotropic Hardening Maximum Extensionb_________$b$Isotropic Hardening Rate ParameterC1________$C_1$Initial Kinematic Hardening ModulusCinf1_____$C_1 / \gamma_1$Kinematic Hardening Parameter Ratio📄 Citation & AcknowledgmentsThis work is part of the research project DigiChrom, funded within the German national initiative MaterialDigital (BMBF).If you use this workflow or codebase in your scientific work, please cite it as follows:Code-Snippet@misc{Harter2026DigiChrom,
  author       = {Harter, Janik and Seifert, Thomas},
  title        = {{DigiChrom: Simulation-based characterization workflow for electroplated coatings}},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub Repository},
  howpublished = {\url{[https://github.com/CMD-HSO/digichrom-sim-workflow](https://github.com/CMD-HSO/digichrom-sim-workflow)}}
}
📧 Contact & LicenseAuthors: Janik Harter, Prof. Dr.-Ing. Thomas SeifertInstitution: Offenburg University of Applied Sciences (HS Offenburg) – Mechanics & Material Digital GroupLicense: Open Source (e.g., MIT License)


<!--

# Projektname

Kurze Beschreibung des Projekts, was es tut und welchen Zweck es erfüllt.

## Inhalt

- [Installation](#installation)
- [Verwendung](#verwendung)
- [Beitrag leisten](#beitrag-leisten)
- [Lizenz](#lizenz)
- [Weitere](#Weitere-mögliche-Punkte-in-der-README)

## Installation

Schritte zur Installation der erforderlichen Software und Abhängigkeiten.

```bash
# Beispielinstallation
git clone https://github.com/dein-benutzername/dein-projekt.git
cd dein-projekt
pip install -r requirements.txt
```

## Verwendung
Kurze Erklärung, wie das Projekt zu nutzen ist, mit möglichen Codebeispielen:
Beispiel für die Verwendung
python src/main.py

## Beitrag leisten

Richtlinien zur Mitwirkung an dem Projekt. Lies auch CONTRIBUTING.md für Details.

## Lizenz

Dieses Projekt steht unter der XX-Lizenz - siehe die Datei LICENSE für Details.

# Weitere Vorlagen und Vorschläge zum Repository
## Repo-Struktur
```markdown
/ (Root)
│
├── README.md                 # Projektbeschreibung und wichtige Infos
├── LICENSE                   # Lizenz des Projekts
├── .gitignore                # Dateien/Ordner, die Git ignorieren soll
├── CONTRIBUTING.md           # Anleitung für Beiträge
├── CODE_OF_CONDUCT.md        # Verhaltenskodex für Mitwirkende
├── CHANGELOG.md              # Änderungsprotokoll
├── requirements.txt          # Liste der Python-Abhängigkeiten (falls erforderlich)
├── setup.py                  # Installation und Paketierung (für Python-Projekte)
├── docs/                     # Dokumentation des Projekts
│   ├── index.md              # Startpunkt für die Dokumentation
│   └── ...                   # Weitere Dokumentationsseiten
├── src/                      # Hauptquellcode des Projekts
│   ├── __init__.py           # Python Paketmarker (falls Python)
│   └── main.py               # Beispielhafte Hauptdatei (kann je nach Programmiersprache anders sein)
├── tests/                    # Test-Module und -Routinen
│   └── test_main.py          # Beispielhafter Test für main.py
├── examples/                 # Beispielanwendungen oder -skripte
│   └── example_usage.py      # Beispielskript zur Nutzung des Projekts
├── scripts/                  # Automatisierungs- und Hilfsskripte
│   └── ci_deploy.sh          # Beispielskript für Continuous Integration/Deployment
└── .github/                  # GitHub-spezifische Metadaten
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md     # Vorlage für Fehlerberichte
    │   └── feature_request.md# Vorlage für Feature-Anfragen
    ├── PULL_REQUEST_TEMPLATE.md # Vorlage für Pull-Requests
    └── workflows/
        └── ci.yml            # Continuous Integration Workflow mit GitHub Actions
```
## Falls notwendig
### CONTRIBUTING.md
```markdown
# Beitrag leisten

Danke, dass Sie zur Verbesserung dieses Projekts beitragen möchten! Hier sind einige Richtlinien:

1. Forken Sie das Projekt.
2. Erstellen Sie einen Feature-Branch: `git checkout -b mein-neues-feature`
3. Machen Sie Ihre Änderungen.
4. Commiten Sie Ihre Änderungen: `git commit -m 'Füge neues Feature hinzu'`
5. Pushen Sie in den Branch: `git push origin mein-neues-feature`
6. Öffnen Sie eine Pull-Request.

Bitte stellen Sie sicher, dass Ihre Beiträge getestet werden und passen Sie sie an unseren Codestyle an.

### Melden von Problemen

Probleme können direkt über die GitHub Issues-Funktion gemeldet werden. Bitte stellen Sie sicher, dass der Fehlerbericht so detailliert wie möglich ist.

```
### Code_OF_CONDUCT.md Verhaltenskodex

```markdown
# Verhaltenskodex

## Unser Versprechen

Als Mitglieder, Mitwirkende und Führungskräfte verpflichten wir uns, die Teilnahme an unserer Community zu einer belästigungsfreien Erfahrung für alle zu machen.

## Unsere Standards

Beispiele für Verhalten, das zu einem positiven Umfeld beiträgt:

- Verwendung einer einladenden und inklusiven Sprache
- Respektieren unterschiedlicher Ansichten und Erfahrungen

## Durchsetzung

Fälle von missbräuchlichem, belästigendem oder anderweitig nicht akzeptablem Verhalten können per E-Mail an das Projektteam gemeldet werden.
```

### CHANGELOG.md

```markdown
# Änderungsprotokoll

Alle signifikanten Änderungen an diesem Projekt werden in diesem Dokument dokumentiert.

## [Unreleased]

### Hinzugefügt
- Neues Feature X

### Geändert
- Update im Feature Y

### Behoben
- Fehler Z behoben

## [1.0.0] - YYYY-MM-TT

### Hinzugefügt
- Initiale Veröffentlichung
```

### ISSUE TEMPLATES bug_report.md
Bug Report (.github/ISSUE_TEMPLATE/bug_report.md):
```markdown
---
name: Bug Report
about: Erstellen Sie einen Bericht, um einen Fehler zu beheben
title: "[BUG] Kurze Beschreibung des Fehlers"
labels: bug
assignees: ''

---

**Beschreiben Sie den Fehler**
Eine klare und prägnante Beschreibung des Fehlers.

**Reproduktion**
Schritte zum Reproduzieren des Verhaltens:
1. Gehe zu '...'
2. Klicke auf '....'
3. Scrolle nach unten zu '....'
4. Siehe Fehler

**Erwartetes Verhalten**
Eine klare und prägnante Beschreibung, was Sie erwartet haben, sollte geschehen.

**Screenshots**
Falls möglich, fügen Sie Screenshots hinzu, um Ihr Problem zu erklären.

**Umgebung (Bitte angeben):**
 - Betriebssystem: [z.B. Windows, Mac, Linux]
 - Browser [z.B. Chrome, Safari]
 - Version [z.B. 22]

**Zusätzliche
```

### PULL_REQUEST_TEMPLATE.md
```markdown
# Pull Request

**Beschreibung**

Beschreiben Sie die vorgenommenen Änderungen und deren Grund.

**Motivation und Kontext**

Warum ist diese Änderung notwendig? Welche Probleme werden dadurch gelöst?

**Änderungen vorgenommen**

Eine kurze Liste der Änderungen, die in dieser Pull-Request enthalten sind:

- Änderung A
- Änderung B
- Änderung C

**Wie wurde es getestet?**

Beschreiben Sie die Tests, die Sie durchgeführt haben, um sicherzustellen, dass Ihre Änderungen korrekt funktionieren:

- Testmethode 1
- Testmethode 2

**Screenshots (falls zutreffend):**

Fügen Sie hier Screenshots hinzu, die die Änderung verdeutlichen.

**Art der Änderung**

- [ ] Fehlerbehebung (nicht-umbruchendes Änderungsprotokoll)
- [ ] Neue Funktion (nicht-umbruchendes Änderungsprotokoll)
- [ ] Änderung zu einer bestehenden Funktion
- [ ] Dies ist eine große, möglicherweise brechende Änderung (fix oder Feature, das das bestehende Funktionalität ändert)

**Checkliste**

- [ ] Code entspricht dem Projekt-Stilguide
- [ ] Dokumentation wurde aktualisiert
- [ ] Changelog wurde aktualisiert
- [ ] Passende Tests wurden hinzugefügt
- [ ] Alle neuen und bestehenden Tests bestehen
```
-->
