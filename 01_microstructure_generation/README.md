# DigiChrom: Module 01 – Microstructure Generation

[![Project: DigiChrom](https://img.shields.io/badge/Project-DigiChrom-blue.svg)](https://github.com/CMD-HSO/digichrom-sim-workflow)
[![Framework: MaterialDigital](https://img.shields.io/badge/Framework-MaterialDigital-green.svg)](https://material-digital.de/)
[![Language: Python 3](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)

This module is dedicated to the automated generation and synthetic reconstruction of representative coating microstructures. 

It provides algorithms to generate complex 2D and 3D geometric models consisting of disperse particle distributions embedded within a continuous matrix phase. The resulting spatial geometries (e.g., exported as STEP files) serve as the structural foundation for subsequent finite element meshing and micromechanical stress analyses in Module 03.

Developed at research group **Computational Mechanics and Digital Materials CMD** of **Offenburg University of Applied Sciences (HSO)** as part of the **DigiChrom** project within the **MaterialDigital** platform.

---

## 📌 Features & Scope

- **Geometric Modeling:** Generation of representative volume elements (RVE) with parametrized particle morphology (size distribution, volume fraction, spatial distribution).
- **Phase Separation:** Explicit geometric definition of matrix and particle boundaries for multi-phase finite element simulations.
- **CAD/FEA Export:** Automated conversion of generated microstructures into standard geometric exchange formats (`.step`, `.sat`).

---

# **Work in progress**

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
