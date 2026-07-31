import os
import subprocess
import shutil
from DPGS.parameter_manager import ParameterManager

class AbaqusSimulation:
    def __init__(self, parameters: ParameterManager, project_path):
        """Initialize Abaqus simulation with the PyIron project."""
        self.params = parameters.get_simulation_parameters()
        self.project_path = project_path
        
        # Default work directory (can be overridden in run_simulation)
        self.abaqus_sim_path = os.path.join(self.project_path, "abaqus_sim")
        
        # Default script path
        self.script_path = os.path.join(self.project_path, "matrix_particle_model.py")
        
    def set_script_path(self, script_path):
        """Allows manually changing the Abaqus script path before running the simulation."""
        self.script_path = script_path


    def copy_script(self):
        """Copy the Abaqus script into the working directory."""
        dest_path = self.abaqus_sim_path
        
        if not os.path.isfile(self.script_path):
            raise FileNotFoundError(f"{self.script_path} does not exist or is not a file.")
        
        try:
            shutil.copy(self.script_path, dest_path)
        except Exception:
            print("Error trying to copy the file.")


    def write_simulation_config(self):
        """Write simulation parameters and project path to a config file for Abaqus to read."""
        config_path = os.path.join(self.abaqus_sim_path, "simulation_config.txt")
        with open(config_path, "w") as f:
            for key, value in self.params.items():
                f.write(f"{key}: {value}\n")


    def run_simulation(self, abaqus_sim_path=None):
        """Execute Abaqus simulation using abaqus.bat."""
        # If a new path is provided, override the default
        if abaqus_sim_path:
            self.abaqus_sim_path = abaqus_sim_path
            os.makedirs(self.abaqus_sim_path, exist_ok=True)

        self.copy_script()
        self.write_simulation_config()  # Save parameters before running

        model_path = os.path.join(self.abaqus_sim_path, "matrix_particle_model.py")
        abaqus_command = [
            r"C:\SIMULIA\Commands\abaqus.bat",
            "cae",
            f"noGUI={model_path}",
        ]

        try:
            result_abaqus = subprocess.run(abaqus_command, capture_output=True, text=True, cwd=self.abaqus_sim_path)
            
            if result_abaqus.returncode == 0:
                print("Abaqus model simulation complete.")
            else:
                print(f"Abaqus failed with error:\n{result_abaqus.stderr}")

        except Exception as e:
            print(f"Error running Abaqus: {e}")

