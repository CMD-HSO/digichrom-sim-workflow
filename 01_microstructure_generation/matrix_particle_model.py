# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import displayGroupOdbToolset as dgo
import regionToolset
import os

# Extract Abaqus parameters from the config
work_dir = os.getcwd()
os.chdir(work_dir)

# Read the simulation configuration from the current directory
config_path = os.path.join(work_dir, "simulation_config.txt") 

simulation_params = {}
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        for line in f:
            key, value = line.strip().split(": ")
            try:
                simulation_params[key] = float(value) if '.' in value else int(value)
            except ValueError:
                simulation_params[key] = value  # Keep as string if conversion fails


matrix_emodulus = simulation_params['matrix_emodulus']
matrix_poisson = simulation_params['matrix_poisson']
particle_emodulus = simulation_params['particle_emodulus']
particle_poisson = simulation_params['particle_poisson']
force_magnitude = simulation_params['force_magnitude']
force_direction = simulation_params['force_direction']
deviationFactor = simulation_params['deviationFactor']
minSizeFactor = simulation_params['minSizeFactor'] 
size = simulation_params['size']

save_path = os.path.join(work_dir, "matrix_particle_sim.cae")

# Model and Step File Paths
model_name = 'MatrixParticleModel'

# Create a new model
model = mdb.Model(name=model_name)

mdb.openStep(
    "../matrix.step"
    , scaleFromFile=OFF)
matrix_part = model.PartFromGeometryFile(combine=False, dimensionality=
    THREE_D, geometryFile=mdb.acis, mergeSolidRegions=True, name=
    'distribution_matrix', type=DEFORMABLE_BODY)
mdb.openStep(
    "../particle_cut.step"
    , scaleFromFile=OFF)
particle_part = model.PartFromGeometryFile(combine=True, dimensionality=
    THREE_D, geometryFile=mdb.acis, mergeSolidRegions=True, name='distribution_particle', 
    type=DEFORMABLE_BODY)# File paths for STEP files


# Matrix material
matrix_material = model.Material(name='MatrixMaterial')
matrix_material.Elastic(table=((matrix_emodulus, matrix_poisson),))

# Particle material
particle_material = model.Material(name='ParticleMaterial')
particle_material.Elastic(table=((particle_emodulus, particle_poisson),))

# Matrix section (Solid section)
matrix_section = model.HomogeneousSolidSection(name='MatrixSection', material='MatrixMaterial')

# Particle section (Solid section)
particle_section = model.HomogeneousSolidSection(name='ParticleSection', material='ParticleMaterial')

# Assign sections to the parts
matrix_part.SectionAssignment(region=(matrix_part.cells,), sectionName='MatrixSection')
particle_part.SectionAssignment(region=(particle_part.cells,), sectionName='ParticleSection')

# Create an assembly and instance the parts
assembly = model.rootAssembly
matrix_instance = assembly.Instance(name='MatrixInstance', part=matrix_part, dependent=ON)
particle_instance = assembly.Instance(name='ParticleInstance', part=particle_part, dependent=ON)

# Merge the parts into a single geometry
merged_part_name = 'MatrixParticle'
merged_part = assembly.InstanceFromBooleanMerge(
    name=merged_part_name,
    instances=(matrix_instance, particle_instance),
    keepIntersections=ON,
    originalInstances=DELETE,  
    domain=GEOMETRY
)

model.parts['MatrixParticle'].setMeshControls(
    elemShape=TET, regions=
    model.parts['MatrixParticle'].cells)

model.parts['MatrixParticle'].Set(cells=model.parts['MatrixParticle'].cells, name='MatrixParticleSet')

model.parts['MatrixParticle'].setElementType(
    elemTypes=(ElemType(elemCode=C3D20R, elemLibrary=STANDARD), ElemType(
    elemCode=C3D15, elemLibrary=STANDARD), ElemType(elemCode=C3D10, 
    elemLibrary=STANDARD)), regions=
    model.parts['MatrixParticle'].sets['MatrixParticleSet'])
                                                                                                 

model.parts['MatrixParticle'].seedPart(
    deviationFactor=deviationFactor, minSizeFactor=minSizeFactor, size=size)

model.parts['MatrixParticle'].generateMesh()

# nodes = model.parts['MatrixParticle'].nodes

# # Define the bounding box for Zmax and Zmin
# z_max = max(node.coordinates[2] for node in nodes)
# z_min = min(node.coordinates[2] for node in nodes)

# tol = 1e-6

# # Select nodes near z_max and z_min using bounding box
# nodes_zmax = nodes.getByBoundingBox(xMin=-1e6, xMax=1e6, yMin=-1e6, yMax=1e6, zMin=z_max - tol, zMax=z_max + tol)
# nodes_zmin = nodes.getByBoundingBox(xMin=-1e6, xMax=1e6, yMin=-1e6, yMax=1e6, zMin=z_min - tol, zMax=z_min + tol)

# # Create sets for Zmax and Zmin nodes
# model.parts['MatrixParticle'].Set(name='ZmaxNodes', nodes=nodes_zmax)
# model.parts['MatrixParticle'].Set(name='ZminNodes', nodes=nodes_zmin)


# # Step creation for static analysis
# model.StaticStep(name='ApplyConcentratedForce', previous='Initial', nlgeom=ON)

# force_magnitude = 1000.0
# force_direction = (0.0, 0.0, 1.0)

# # Apply the concentrated force on ZmaxNodes (forces in Z direction)
# model.ConcentratedForce(name='ConcentratedForce', createStepName='ApplyConcentratedForce', 
#                           region=model.rootAssembly.instances['MatrixParticle-1'].sets['ZmaxNodes'], 
#                           cf1=force_magnitude * force_direction[0], 
#                           cf2=force_magnitude * force_direction[1], 
#                           cf3=force_magnitude * force_direction[2])

# # Boundary condition for ZminNodes (fixed in all directions)
# model.DisplacementBC(name='FixZminNodes', createStepName='ApplyConcentratedForce', 
#                       region=model.rootAssembly.instances['MatrixParticle-1'].sets['ZminNodes'], 
#                       u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0)



# Get all faces in the part
part = model.parts['MatrixParticle']
faces = part.faces

tol = 1e-6

# Compute Zmax and Zmin based on face centroids
z_max = max(face.pointOn[0][2] for face in faces)
z_min = min(face.pointOn[0][2] for face in faces)

# Select faces near z_max and z_min using bounding box
faces_zmax = faces.getByBoundingBox(xMin=-1e6, xMax=1e6, yMin=-1e6, yMax=1e6, zMin=z_max - tol, zMax=z_max + tol)
faces_zmin = faces.getByBoundingBox(xMin=-1e6, xMax=1e6, yMin=-1e6, yMax=1e6, zMin=z_min - tol, zMax=z_min + tol)

# Create sets for Zmax and Zmin faces
part.Set(name='ZmaxFaces', faces=faces_zmax)
part.Set(name='ZminFaces', faces=faces_zmin)

# Create step for static analysis
model.StaticStep(name='ApplyPressureLoad', previous='Initial', nlgeom=ON)

# Reference the assembly instance
assembly = model.rootAssembly
instance = assembly.instances['MatrixParticle-1']

assembly.Surface(name='ZmaxSurface', side1Faces=instance.sets['ZmaxFaces'].faces)
assembly.Surface(name='ZminSurface', side1Faces=instance.sets['ZminFaces'].faces)

region_zmax = assembly.surfaces['ZmaxSurface'] 
region_zmin = regionToolset.Region(faces=instance.sets['ZminFaces'].faces) 


model.Pressure(
    name='PressureLoad',
    createStepName='ApplyPressureLoad',
    region=region_zmax,
    magnitude=force_magnitude,
    distributionType=UNIFORM
)

model.DisplacementBC(
    name='FixZminFaces',
    createStepName='ApplyPressureLoad',
    region=region_zmin,
    u1=0.0, u2=0.0, u3=0.0,
    ur1=0.0, ur2=0.0, ur3=0.0
)

# Create a job
job_name = 'MatrixParticleSimulation'
job = mdb.Job(name=job_name, model=model_name, type=ANALYSIS, 
              explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, 
              description='Matrix-Particle Simulation Job')

job.submit()
job.waitForCompletion()

# odb_file = f'{job_name}.odb' # usable for higher abaqus version than 2023
odb_file = '%s.odb'%(job_name) # for abaqus version 2023
odb = session.openOdb(name=odb_file)
mdb.saveAs(pathName=save_path)

viewport = session.viewports['Viewport: 1']
viewport.setValues(displayedObject=odb)
 
viewport.setValues(
    width=400, 
    height=300 
)


viewport.odbDisplay.commonOptions.setValues(visibleEdges=NONE)

viewport.odbDisplay.setValues(viewCutNames=('X-Plane', ), viewCut=ON)
viewport.odbDisplay.viewCuts['X-Plane']
viewport.view.setValues(session.views['Right'])
viewport.view.rotate(90, (0,0,1))
viewport.view.fitView()

cmap = session.viewports['Viewport: 1'].colorMappings['Material']
session.viewports['Viewport: 1'].setColor(colorMapping=cmap)

session.printToFile(
    fileName=os.path.join(work_dir, 'section_cut_color.png'),
    format=PNG,
    canvasObjects=(viewport,)
)

viewport.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
viewport.odbDisplay.contourOptions.setValues(intervalType=LOG)

session.printToFile(
    fileName=os.path.join(work_dir, 'section_cut.png'),
    format=PNG,
    canvasObjects=(viewport,)
)


session.linkedViewportCommands.setValues(_highlightLinkedViewports=True)
leaf = dgo.LeafFromOdbElementMaterials(elementMaterials=("PARTICLEMATERIAL", ))
viewport.odbDisplay.displayGroup.replace(leaf=leaf)
dg = viewport.odbDisplay.displayGroup
dg = session.DisplayGroup(name='ParticleDisplay', objectToCopy=dg)
viewport.odbDisplay.setValues(visibleDisplayGroups=(dg, ))

session.printToFile(
    fileName=os.path.join(work_dir, 'particle_cut.png'),
    format=PNG,
    canvasObjects=(viewport,)
)

viewport.odbDisplay.setValues(viewCutNames=('X-Plane', ), viewCut=OFF)
viewport.odbDisplay.setValues(visibleDisplayGroups=(dg, ))
viewport.view.rotate(-45, (1,0,0))
viewport.view.rotate(45, (0,1,1))
viewport.view.fitView()


session.printToFile(
    fileName=os.path.join(work_dir, 'particle_iso.png'),
    format=PNG,
    canvasObjects=(viewport,)
)

odb.close()
