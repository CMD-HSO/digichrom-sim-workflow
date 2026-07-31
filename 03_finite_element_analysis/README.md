# DigiChrom: Finite Element Analysis & Micromechanical Evaluation

[![Project: DigiChrom](https://img.shields.io/badge/Project-DigiChrom-blue.svg)](https://github.com/CMD-HSO/digichrom-sim-workflow)
[![Framework: MaterialDigital](https://img.shields.io/badge/Framework-MaterialDigital-green.svg)](https://material-digital.de/)
[![Language: Python 3](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)
[![FE Solver: Abaqus](https://img.shields.io/badge/FEA-Abaqus-red.svg)](https://www.3ds.com/products-services/simulia/products/abaqus/)

This module provides tools for setting up 3D representative volume/matrix-particle FE models in Dassault Systèmes Abaqus, executing stress analyses, extracting integration point data, and evaluating micromechanical stress distributions (e.g., maximum principal stresses in particles vs. matrix).

Developed at research group **Computational Mechanics and Digital Materials CMD** of **Offenburg University of Applied Sciences (HSO)** as part of the **DigiChrom project** within the **MaterialDigital** platform.

---

## 📌 Overview

The workflow covers the pipeline from CAD/STEP-based Abaqus model build to statistical post-processing:

1. **Model Generation & Simulation Setup:** Automatically imports geometry (`matrix.step`, `particle_cut.step`), assigns material parameters from a configuration file, generates 3D solid meshes (C3D10/C3D15/C3D20R), applies displacement boundary conditions, and runs the Abaqus FE job.
2. **Data Extraction:** Extracts element integration point field outputs (Stress tensor, Maximum Principal Stress, Integration Point Volume `IVOL`) per region (`MATRIXSET` and `PARTICLESET`) directly from the Abaqus `.odb` file.
3. **Statistical Post-Processing:** Evaluates volume-weighted stress distributions, calculates key statistical metrics (mean, median, 5th/95th percentiles), and renders histogram plots for both phases.

---

## 📁 Repository Structure

### Python & Abaqus Scripts
- `matrix_particle_model.py`: Abaqus Python script for building the FE model from STEP files, applying boundary conditions, generating the mesh, executing the FE analysis, and saving cross-section plots.
- `DataExportFromABAQUSElements_CMDHSO_260731.py`: Abaqus Python post-processing script to export stress and volume data (`IVOL`) from specified element sets/instances out of the `.odb` file into `.dat` files.
- `Evaluate_Data.py`: Python script for reading exported `.dat` files, calculating phase volume fractions, performing statistical evaluations (Mean, Median, 5th/95th Percentiles), and generating stress distribution histograms.

### Configuration & Inputs (Expected)
- `simulation_config.txt`: Key-value configuration file containing material properties (Young's modulus, Poisson's ratio for matrix and particles) and mesh control parameters.
- `../matrix.step` & `../particle_cut.step`: Input geometry STEP files for the matrix and particle domains. Obtained form "01_microstructure_generation".

### Execution & Batch Scripts
- `Workflow*.bat`: Windows batch script automating the execution of Abaqus post-processing extraction for both `MATRIXSET` and `PARTICLESET` and managing output file renaming (`Data4Analysis_E_MATRIX.dat` and `Data4Analysis_E_PARTICLE.dat`).


---

## ⚙️ Workflow Execution

### Step 1: Model Build & FE Analysis
Run the model generation and simulation execution script inside Abaqus:
`abaqus cae noGUI=matrix_particle_model.py`

*Note: This reads parameters from `simulation_config.txt` and exports `MatrixParticleSimulation.odb` upon completion.*

### Step 2: Data Extraction (Post-Processing)
Run the provided batch file to execute the element data export via Abaqus Python for both matrix and particle sets:
`Workflow.bat`

This generates two key datasets:
- `Data4Analysis_E_MATRIX.dat`
- `Data4Analysis_E_PARTICLE.dat`

### Step 3: Statistical Evaluation & Visualization
Execute the stand-alone evaluation script to compute statistics and plot histograms:
`python Evaluate_Data.py`

---

## 📊 Outputs & Generated Artifacts

- **`Fig_PARTICLE_sigI.png`**: Histogram showing maximum principal stress distribution within the particle phase with marked mean, median, and 5th/95th percentiles.
- **`Fig_MATRIX_sigI.png`**: Histogram showing maximum principal stress distribution within the matrix phase.
- **`section_cut.png` / `particle_iso.png`**: Rendered PNG images of contour plots and section cuts of the analyzed FE mesh.

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
