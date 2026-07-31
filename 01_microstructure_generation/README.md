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