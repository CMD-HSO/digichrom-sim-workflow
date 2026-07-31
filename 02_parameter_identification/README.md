# DigiChrom: Simulation-Based Parameter Identification Workflow

[![Project: DigiChrom](https://img.shields.io/badge/Project-DigiChrom-blue.svg)](https://www.material-digital.de/project/25)
[![Framework: MaterialDigital](https://img.shields.io/badge/Framework-MaterialDigital-green.svg)](https://material-digital.de/)
[![Language: Python 3](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)
[![FE Solver: Abaqus](https://img.shields.io/badge/FEA-Abaqus-red.svg)](https://www.3ds.com/products-services/simulia/products/abaqus/)

Automated workflow for identifying non-linear elasto-plastic constitutive material parameters (combined kinematic and isotropic hardening) of electroplated coatings based on instrumented indentation testing (nano/micro-indentation) and Finite Element Analysis (FEA).

Developed at research group **Computational Mechanics and Digital Materials CMD** of **Offenburg University of Applied Sciences (HSO)** as part of the **DigiChrom** project within the **MaterialDigital** platform.

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

1. Experimental Data (.txt) -> (Time, Force, Displacement)
2. Main Optimization Loop (Python / SLSQP):
   - Sample / Update Material Parameters of plasticity model (Re, Qinf, b, C, gamma)
   - Write Abaqus Include Files (indent_para.inp, indent_mat.inp, ...)
   - Execute FEA Solver (Abaqus Job Execution)
   - Extract Reaction Forces & Displacements via Post-Processing Script
   - Compute Least-Squares Objective Function (Exp vs. Sim)
3. Output -> Optimized Parameter Set & Fitted Curves 

---

## 📁 Repository Structure

- _IndPlast_Seifert_250601b.py: Main optimization script (parameter setup & SLSQP execution)
- DriveModel_Seifert_250301.py: Interface handling Abaqus input generation, execution & post-processing
- ParameterStructure_Seifert.py: Data structure managing parameter bounds, mapping & scaling
- PlotResults_Seifert.py: Utility module for plotting experimental vs. simulated curves
- _postProc_IndPlast_Seifert.py: Abaqus post-processing script (extracts load-displacement data)
- indent_glob.inp: Base Abaqus FE mesh and boundary condition template
- data_indent.txt: Sample experimental indentation dataset
- README.md: Documentation

---

## 🚀 Requirements & Installation

### Prerequisites
1. **Python 3.x** with the required mathematical and scientific libraries:
   - numpy
   - scipy
   - matplotlib
2. **Dassault Systèmes Abaqus** (must be installed and accessible via system CLI command `abaqus`).

### Running the Workflow
1. Clone the repository:
   `git clone https://github.com/CMD-HSO/digichrom-sim-workflow.git`
   `cd digichrom-sim-workflow`

2. Ensure your experimental data file (`data_indent.txt`) contains four columns formatted as follows:
   - Column 0: Time ($t$)
   - Column 1: Measured Reaction Force ($F_{\text{exp}}$)
   - Column 2: Controlled Displacement ($u_{\text{cntr}}$)
   - Column 3: Temperature ($T$)

3. Launch the parameter optimization process:
   `python _IndPlast_Seifert_250601b.py`

---

## 🔬 Constitutive Model Parameters

The workflow optimizes non-linear elasto-plastic parameters for **combined hardening**:

| Parameter | Symbol | Description |
| :--- | :--- | :--- |
| E_________ | $E$ | Young's Modulus |
| nue_______ | $\nu$ | Poisson's Ratio |
| Re________ | $\sigma_0$ / $R_e$ | Initial Yield Stress |
| Qinf______ | $Q_{\infty}$ | Isotropic Hardening Maximum Extension |
| b_________ | $b$ | Isotropic Hardening Rate Parameter |
| C1________ | $C_1$ | Initial Kinematic Hardening Modulus |
| Cinf1_____ | $C_1 / \gamma_1$ | Kinematic Hardening Parameter Ratio |

---

## 📄 Citation & Acknowledgments

This research is part of the DigiChrom project, funded within the German national initiative MaterialDigital by the German Federal Ministry of Research, Technology and Space (BMFTR) (grant number 13XP5195I).

If you use this workflow or code in your research, please cite it as:

```bibtex
@misc{Harter2026DigiChrom,
  author       = {Harter, Janik and Seifert, Thomas},
  title        = {{DigiChrom: Simulation-based characterization workflow for electroplated coatings}},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub Repository},
  howpublished = {\url{[https://github.com/CMD-HSO/digichrom-sim-workflow](https://github.com/CMD-HSO/digichrom-sim-workflow)}}
}
