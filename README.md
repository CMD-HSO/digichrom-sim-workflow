# DigiChrom: Integrated Simulation-Based Characterization Workflow

[![Project: DigiChrom](https://img.shields.io/badge/Project-DigiChrom-blue.svg)](https://github.com/CMD-HSO/digichrom-sim-workflow)
[![Framework: MaterialDigital](https://img.shields.io/badge/Framework-MaterialDigital-green.svg)](https://material-digital.de/)
[![Language: Python 3](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)
[![FE Solver: Abaqus](https://img.shields.io/badge/FEA-Abaqus-red.svg)](https://www.3ds.com/products-services/simulia/products/abaqus/)

This repository contains the integrated modular simulation workflow for electroplated coatings developed at the research group **Computational Mechanics and Digital Materials CMD** of **Offenburg University of Applied Sciences (HSO)** within the **DigiChrom** initiative (MaterialDigital).

---

## 🏗️ Workflow Architecture

The characterization framework is structured into three sequential modules:

1. **`01_microstructure_generation/`** 
   Generating synthetic or experimental-based digital representations of coating microstructures.
   
2. **`02_parameter_identification/`** 
   Automated calibration of non-linear elasto-plastic constitutive parameters (combined hardening) via FEA-coupled optimization using experimental indentation data.
   
3. **`03_finite_element_analysis/`** 
   Application of identified material models to full-scale component simulations and micromechanical failure evaluation.

---

## 📄 Citation & Acknowledgments

This research is part of the **DigiChrom** project, funded within the German national initiative **MaterialDigital** by the German Federal Ministry of Research, Technology and Space (BMFTR) (grant number 13XP5195I).

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
