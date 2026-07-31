from pyiron import Project
from DPGS.parameter_manager import ParameterManager
from DPGS.generate_particle import ParticleGenerator
from DPGS.abaqus_simulation import AbaqusSimulation

class ExtendedProject(Project):
    
    def __init__(self, project_name):
        super().__init__(project_name)
        self.project_path = self.path  # Store project directory
        self.params = ParameterManager()  # Internal Parameter Manager
        self.abaqus_simulation = AbaqusSimulation(self.params, self.project_path)

    def get_project_path(self):
        """Returns the current project's directory for exporting files."""
        return self.project_path

    def set_particle_parameters(self, **kwargs):
        """Set particle generation parameters inside the project."""
        self.params.set_particle_parameters(**kwargs)
        
    def set_simulation_parameters(self, **kwargs):
        """Set particle simulation parameters inside the project."""
        self.params.set_simulation_parameters(**kwargs)

    def create_particle(self):
        """Creates and returns a ParticleGenerator instance using stored parameters."""
        self.particles = ParticleGenerator(self.params, self.project_path)
        self.particles.generate_particle()
        return self.particles
    
    def run_abaqus(self, abaqus_sim_path=None):
        """Run the Abaqus simulation inside the PyIron project."""
        self.abaqus_simulation.run_simulation(abaqus_sim_path=abaqus_sim_path)