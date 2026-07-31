import os
from DPGS import ExtendedProject

# Initialize PyIron Extended Project
pr = ExtendedProject("../particle_project")


pr.set_particle_parameters(
            bbox = [0, 100, 0, 100, 0, 100],
            num_seeds = 18,
            distribution = 'exponential',
            gradient_factor = 3.0
        )

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


for num in range(1, 4):
    print(f"Running iteration {num}")

    try:
        particle = pr.create_particle()
        if not particle:
            print(f"Iteration {num}: Failed to create particle, skipping...")
            continue  # Skip to next iteration

        particle.export_all_geom()
        particle.compute_export_statistics()

        pr.abaqus_simulation.set_script_path(script_path="matrix_particle_model.py")

        abaqus_sim_path = os.path.join(particle.output_folder, "abaqus_sim")

        try:
            pr.run_abaqus(abaqus_sim_path)
        except Exception as e:
            print(f"Iteration {num}: run_abaqus() failed: {e}, skipping...")
            continue  # Skip to next iteration

    except Exception as e:
        print(f"Iteration {num}: create_particle() failed: {e}, skipping...")
        continue  # Skip to next iteration

    print(f"Iteration {num} completed successfully.")
    
    
    
pr2 = ExtendedProject("../particle_project2")


pr2.set_particle_parameters(
            bbox = [0, 100, 0, 100, 0, 100],
            num_seeds = 18,
            distribution = 'exponential',
            gradient_factor = 3.0
        )

pr2.set_simulation_parameters(
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


for num in range(1, 4):
    print(f"Running iteration {num}")

    try:
        particle2 = pr2.create_particle()
        if not particle:
            print(f"Iteration {num}: Failed to create particle, skipping...")
            continue  # Skip to next iteration

        particle2.export_all_geom()
        particle2.compute_export_statistics()

        pr2.abaqus_simulation.set_script_path(script_path="matrix_particle_model.py")

        abaqus_sim_path2 = os.path.join(particle2.output_folder, "abaqus_sim")

        try:
            pr2.run_abaqus(abaqus_sim_path2)
        except Exception as e:
            print(f"Iteration {num}: run_abaqus() failed: {e}, skipping...")
            continue  # Skip to next iteration

    except Exception as e:
        print(f"Iteration {num}: create_particle() failed: {e}, skipping...")
        continue  # Skip to next iteration

    print(f"Iteration {num} completed successfully.")


# particle = pr.create_particle()

# particle.export_all_geom()

# particle.compute_export_statistics()

# pr.abaqus_simulation.set_script_path(script_path = "matrix_particle_model.py")

# abaqus_sim_path = os.path.join(particle.output_folder, "abaqus_sim")

# pr.run_abaqus(abaqus_sim_path)