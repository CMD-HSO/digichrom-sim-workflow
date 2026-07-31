class ParameterManager:
    def __init__(self):
        # Default parameters for particle generation
        self.particle_params = {
            'bbox': [0, 10, 0, 10, 0, 10],
            'num_seeds': 100,
            'distribution': 'uniform',
            'gradient_factor': 1.0
        }
        
        # Default parameters for simulations
        self.simulation_params = {
            # Simulation parameter
            'matrix_emodulus' : 200e3,
            'matrix_poisson' : 0.3,
            'particle_emodulus' : 300e3,
            'particle_poisson' : 0.25,
            # Define the concentrated force magnitude and direction
            'force_magnitude' : 1000.0,
            'force_direction' : (0.0, 0.0, 1.0),
            # Mesh
            'deviationFactor': 0.1,
            'minSizeFactor': 0.1 , 
            'size': 100  
        }

    def set_particle_parameters(self, **kwargs):
        """Update particle parameters with user-defined values."""
        self.particle_params.update(kwargs)

    def set_simulation_parameters(self, **kwargs):
        """Update simulation parameters with user-defined values."""
        self.simulation_params.update(kwargs)

    def get_particle_parameters(self):
        """Return current particle generation parameters."""
        return self.particle_params

    def get_simulation_parameters(self):
        """Return current simulation parameters."""
        return self.simulation_params