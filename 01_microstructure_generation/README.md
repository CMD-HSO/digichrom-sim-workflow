# DigiChrom: Microstructure Generation

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

## 📌 Acknowledgments & Origin

This research is part of the DigiChrom project, funded within the German national initiative MaterialDigital by the German Federal Ministry of Research, Technology and Space (BMFTR) (grant number 13XP5195I).

This module is directly based on and incorporates the **DPGS (Dispersion Particle Generator and Simulation)** framework developed by **Thitichai Janpheng** ('tjanp').

- **Original Repository:** [tjanp/DPGS-Dispersion-Particle-Generator-and-Simulation](https://github.com/tjanp/DPGS-Dispersion-Particle-Generator-and-Simulation)

If you use this workflow or code in your research, please cite it as:

```bibtex
@misc{Janpheng2026DigiChrom,
  author       = {Janpheng, Thitichai and Harter, Janik and Seifert, Thomas},
  title        = {{DigiChrom: Simulation-based characterization workflow for electroplated coatings (Microstructure generation)}},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub Repository},
  howpublished = {\url{[https://github.com/CMD-HSO/digichrom-sim-workflow/tree/main/01_microstructure_generation](https://github.com/CMD-HSO/digichrom-sim-workflow/tree/main/01_microstructure_generation)}}
}
```

# DPGS-Dispersion-Particle-Generator-and-Simulation

## Overview
This project generates randomly distributed particles within a defined bounding box. 
The process begins by selecting seed points, which are distributed within the box. For each seed point, a bounding sphere is created based on an voronois diagram, spheres are fitted inside the voronoi cell. 
Inside each generated bounding sphere, random points are generated on the surface of the sphere, and a convex hull is created from these points.
Using CadQuery, the convex hull particles are converted into solid geometries, which are then subtracted from the corresponding bounding box solid. 
Afterward, both the particle data and the resulting geometry (after subtraction) are exported to STEP files for use in Abaqus simulations.

## Setup and Usage

To install all dependencies, open Anaconda Prompt as administrator and run the following commands:

```bash
cd C:\Users\User\Desktop\DPGS-Dispersion-Particle-Generator-and-Simulation
conda env create --prefix ./env -f env.yml
```

Install Manually in chronological order:
```bash
cd C:\Users\User\Desktop\DPGS-Dispersion-Particle-Generator-and-Simulation
conda create --prefix ./env python=3.12 numpy scipy matplotlib cadquery pyiron pyiron_atomistics -c conda-forge -y
conda activate ./env
conda export --prefix ./env > env.yml
```

To adjust the model in Abaqus, make changes in `matrix_particle_model.py`.

### Creating new project
```bash
pr = ExtendedProject("../particle_project")
```

### Set parameters for particle generation 
```bash
pr.set_particle_parameters(
            bbox = [0, 100, 0, 100, 0, 100],
            num_seeds = 18,
            distribution = 'exponential',
            gradient_factor = 3.0
        )
```

### Set parameters for abaqus simulation
```bash
pr.set_simulation_parameters(
            matrix_emodulus = 150e3,
            matrix_poisson = 0.25,
            particle_emodulus = 250e3,
            particle_poisson = 0.2,
            force_magnitude = 1000.0,
            force_direction = (0.0, 0.0, 1.0),
            deviationFactor=0.1,
            minSizeFactor=0.1, 
            size=100 
            )
```

### Create particle
```bash
particle = pr.create_particle()
```

### Exporting stl and step files of the particles
```bash
particle.export_all_geom()
```

### Compute and export statistics of the particles
```bash
particle.compute_export_statistics()
```

### Select simulation script to build the simulation model
```bash
pr.abaqus_simulation.set_script_path(script_path = "matrix_particle_model.py")
```

### Set where simulation data should be exported
```bash
pr.abaqus_simulation.set_script_path(script_path = "matrix_particle_model.py")
```

### Run abaqus simulation
```bash
pr.run_abaqus(abaqus_sim_path)
```
