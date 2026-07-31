from pyiron_base import Project
import os

# ==============================================================================
# 0. PYIRON PROJEKT-INITIALISIERUNG
# ==============================================================================
# Erstellt einen Projekt-Ordner & HDF5-Datenbank zur FAIRen Datenverwaltung
pr = Project("DigiChrom_Workflow")

# Pfade zu euren Modul-Ordnern
BASE_DIR = os.getcwd()
DIR_01_MICRO = os.path.join(BASE_DIR, "01_microstructure_generation")
DIR_02_PARAM = os.path.join(BASE_DIR, "02_parameter_identification")
DIR_03_FEA   = os.path.join(BASE_DIR, "03_finite_element_analysis")


# ==============================================================================
# 1. MODUL 01: MICROSTRUCTURE GENERATION
# ==============================================================================
print(">>> Step 1: Microstructure Generation")

def run_microstructure_gen(job):
    """
    Funktion zur Erzeugung der CAD/STEP-Geometrien (Particle & Matrix)
    """
    import subprocess
    # Beispiel: Aufruf deines Geometrie-Generators in 01_microstructure_generation
    # (Erzeugt matrix.step und particle_cut.step)
    cmd = "python generate_geometry.py"
    subprocess.run(cmd, shell=True, cwd=DIR_01_MICRO, check=True)
    
    # Ausgaben im pyiron HDF5-Speicher ablegen
    job.data["step_matrix"] = os.path.join(DIR_01_MICRO, "matrix.step")
    job.data["step_particle"] = os.path.join(DIR_01_MICRO, "particle_cut.step")

# Erstellung eines pyiron PythonJobs für Modul 01
job_micro = pr.create_job(pr.job_type.PythonJob, "job_01_microstructure")
job_micro.python_function = run_microstructure_gen
job_micro.run()


# ==============================================================================
# 2. MODUL 02: PARAMETER IDENTIFICATION (Indentation & SLSQP)
# ==============================================================================
print(">>> Step 2: Parameter Identification")

def run_parameter_identification(job):
    """
    Koppelt FEA-Abaqus Indentation mit scipy.optimize (SLSQP)
    """
    import sys
    sys.path.append(DIR_02_PARAM)
    
    # Import eures Haupt-Optimierungsskripts aus 02_parameter_identification
    import _IndPlast_CMDHSO_260731 as opt_module
    
    # Ausführung der Parameteridentifikation
    # (Optimierung von E, nue, Re, Qinf, b, C1, Cinf1)
    calibrated_params = opt_module.run_optimization()
    
    # Ergebnisse direkt im pyiron HDF5-Data-Container speichern
    job.data["calibrated_parameters"] = calibrated_params

job_param = pr.create_job(pr.job_type.PythonJob, "job_02_parameter_id")
job_param.run()


# ==============================================================================
# 3. MODUL 03: FINITE ELEMENT ANALYSIS & POST-PROCESSING
# ==============================================================================
print(">>> Step 3: Component FEA & Evaluation")

# 3a. Parameterübergabe aus Modul 02 auslesen
calibrated_mat = job_param.data["calibrated_parameters"]

def run_fea_and_eval(job):
    """
    1. Schreibt simulation_config.txt mit identifizierten Materialwerten
    2. Startet Abaqus Simulation (matrix_particle_model.py)
    3. Führt Post-Processing (Evaluate_Data.py) aus
    """
    import subprocess
    
    # Config für Abaqus schreiben
    config_file = os.path.join(DIR_03_FEA, "simulation_config.txt")
    with open(config_file, "w") as f:
        f.write(f"matrix_emodulus: {calibrated_mat.get('E_matrix', 210000.0)}\n")
        f.write(f"matrix_poisson: {calibrated_mat.get('nu_matrix', 0.3)}\n")
        f.write(f"particle_emodulus: {calibrated_mat.get('E_particle', 400000.0)}\n")
        f.write(f"particle_poisson: {calibrated_mat.get('nu_particle', 0.2)}\n")
        f.write("force_magnitude: 1000.0\n")
        f.write("deviationFactor: 0.1\n")
        f.write("minSizeFactor: 0.1\n")
        f.write("size: 2.0\n")
    
    # 1. Abaqus CAE Simulation starten
    cmd_abaqus = "abaqus cae noGUI=matrix_particle_model.py"
    subprocess.run(cmd_abaqus, shell=True, cwd=DIR_03_FEA, check=True)
    
    # 2. Data Extraction Batch ausführen
    cmd_batch = "Workflow.bat"
    subprocess.run(cmd_batch, shell=True, cwd=DIR_03_FEA, check=True)
    
    # 3. Auswertung / Histogramme generieren
    cmd_eval = "python Evaluate_Data.py"
    subprocess.run(cmd_eval, shell=True, cwd=DIR_03_FEA, check=True)

job_fea = pr.create_job(pr.job_type.PythonJob, "job_03_fea_eval")
job_fea.run()


# ==============================================================================
# 4. WORKFLOW SUMMARY & ERGEBNIS-ZUSAMMENFASSUNG
# ==============================================================================
print("\n==========================================")
print("     DIGICHROM WORKFLOW COMPLETED         ")
print("==========================================")
print("Saved Jobs in pyiron database:")
print(pr.job_table())