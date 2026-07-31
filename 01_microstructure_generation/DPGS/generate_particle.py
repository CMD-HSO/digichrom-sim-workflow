import os
import random
import cadquery as cq
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, ConvexHull, cKDTree
from datetime import datetime
from DPGS.parameter_manager import ParameterManager

class ParticleGenerator:
    def __init__(self, parameters: ParameterManager, project_path):
        self.parameters = parameters
        self.particle_list = []
        self.centroid_list = []
        self.diameter_array = []
        self.nn_dist = []
        self.r_nn_dist = []
        
        # Set output folder
        self.project_path = project_path
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_folder = os.path.join(self.project_path, f"generated_particle_{self.timestamp}")
        os.makedirs(self.output_folder, exist_ok=True)
          

    def generate_points(self):
        """Function to generate random points within the bounding box with different distributions"""
        self.params = self.parameters.get_particle_parameters()
        self.bbox = self.params['bbox']
        self.num_seeds = self.params['num_seeds']
        self.distribution = self.params['distribution']
        self.gradient_factor = self.params['gradient_factor']
        
        xmin, xmax, ymin, ymax, zmin, zmax = self.bbox
        points = []
        
        for _ in range(self.num_seeds):
            x = random.uniform(xmin, xmax)
            y = random.uniform(ymin, ymax)
            
            if self.distribution == 'uniform':
                z = random.uniform(zmin, zmax)
            elif self.distribution == 'linear':
                t = random.random()
                z = np.interp(t ** (1 / self.gradient_factor), [0, 1], [zmax, zmin])
            elif self.distribution == 'exponential':
                z = random.expovariate(1 / (zmax - zmin) * self.gradient_factor)
                z = np.clip(z, zmin, zmax)
            else:
                raise ValueError("Invalid distribution type.")
            
            points.append((x, y, z))
        
        return points


    def generate_particle(self):
        """Generate sphere convex hulls from Voronoi diagram"""
        seeds = self.generate_points()
        vor = Voronoi(seeds)

        self.particle_list = []
        self.centroid_list = []
        self.radius_list = []
        xmin, xmax, ymin, ymax, zmin, zmax = self.bbox
        
        for i, region in enumerate(vor.regions):
            if -1 in region or len(region) == 0:
                continue

            try:
                centroid, radius = compute_cell_radius(region, vor.vertices)

                if not (xmin <= centroid[0] <= xmax and
                        ymin <= centroid[1] <= ymax and
                        zmin <= centroid[2] <= zmax):
                    continue

                sphere_points = generate_points_on_sphere(centroid, radius)
                hull = ConvexHull(sphere_points)

                vertices = sphere_points[hull.vertices]
                faces = hull.simplices

                solid = convert_to_solid(vertices, faces)
                self.particle_list.append(solid)
                self.centroid_list.append(centroid)
                self.radius_list.append(radius)
                
                print(i, "seeds were processed")
            
            except Exception as e:
                print(f"Error processing region {i}: {e}")
                continue
            
        centroid_array = np.array(self.centroid_list)
        radius_array = np.array(self.radius_list)

        kdtree = cKDTree(centroid_array)

        # Calculate distances between centroids
        self.nn_dist = np.zeros(len(centroid_array))  
        for i, point in enumerate(centroid_array):
            dist, idx = kdtree.query(point, k=2)
            self.nn_dist[i] = dist[1]
            
        # Calculate distance between centroids - radius
        self.r_nn_dist = np.zeros(len(centroid_array))  
        for i, point in enumerate(centroid_array):
            dist, idx = kdtree.query(point, k=2)
            r_dist = dist[1] - radius_array[idx[0]] - radius_array[idx[1]]
            self.r_nn_dist[i] = r_dist
        
        self.diameter_array = radius_array * 2

        return self.particle_list, self.diameter_array, self.nn_dist, self.r_nn_dist


    def export_all_geom(self):
        output_folder = self.output_folder
        xmin, xmax, ymin, ymax, zmin, zmax = self.bbox
        particle_list = self.particle_list

        if not particle_list:
            print("No particles generated, skipping export.")
            return

        # Combine all particles into one shape
        combined_particles = cq.Compound.makeCompound(particle_list)

        # Export raw particle geometry
        cq.exporters.export(combined_particles, os.path.join(output_folder, 'particles.stl'))
        cq.exporters.export(combined_particles, os.path.join(output_folder, 'particle.step'))

        # Define bounding box dimensions
        box_length = xmax - xmin
        box_width = ymax - ymin
        box_height = zmax - zmin

        # Create bounding box **aligned to bbox bounds**
        bounding_box = (
            cq.Workplane("XY")
            .box(box_length, box_width, box_height, centered=(False, False, False))  # No automatic centering
            .translate((xmin, ymin, zmin))  # Position to match bbox
        )

        # Intersection (particles inside bounding box)
        try:
            particle_cut = bounding_box.intersect(combined_particles)
            cq.exporters.export(particle_cut, os.path.join(output_folder, 'particle_cut.stl'))
            cq.exporters.export(particle_cut, os.path.join(output_folder, 'particle_cut.step'))
        except Exception as e:
            print(f"Error creating particle_cut: {e}")

        # Subtract particles from bounding box (matrix geometry)
        try:
            matrix = bounding_box.cut(combined_particles)
            cq.exporters.export(matrix, os.path.join(output_folder, 'matrix.stl'))
            cq.exporters.export(matrix, os.path.join(output_folder, 'matrix.step'))
        except Exception as e:
            print(f"Error creating matrix: {e}")


    def compute_export_statistics(self):
        diameter_list = self.diameter_array
        nn_dist = self.nn_dist
        r_nn_dist = self.r_nn_dist
        output_folder = self.output_folder
        
        # Create the text file with statistics
        statistics_file_path = os.path.join(output_folder, 'particle_statistics.txt')
        with open(statistics_file_path, 'w') as f:
            f.write(f"Number of particles: {len(diameter_list)}\n\n")
            
            
    def compute_export_statistics(self):
        diameter_list = self.diameter_array
        nn_dist = self.nn_dist
        r_nn_dist = self.r_nn_dist
        output_folder = self.output_folder
        
        # Calculate statistics for diameter_list
        mean_diameter = np.mean(diameter_list)
        max_diameter = np.max(diameter_list)
        min_diameter = np.min(diameter_list)
        variance_diameter = np.var(diameter_list)
        std_deviation_diameter = np.std(diameter_list)

        # Calculate statistics for nn_dist
        mean_nn_dist = np.mean(nn_dist)
        max_nn_dist = np.max(nn_dist)
        min_nn_dist = np.min(nn_dist)
        variance_nn_dist = np.var(nn_dist)
        std_deviation_nn_dist = np.std(nn_dist)

        # Calculate statistics for r_nn_dist
        mean_r_nn_dist = np.mean(r_nn_dist)
        max_r_nn_dist = np.max(r_nn_dist)
        min_r_nn_dist = np.min(r_nn_dist)
        variance_r_nn_dist = np.var(r_nn_dist)
        std_deviation_r_nn_dist = np.std(r_nn_dist)

        segments = 20

        # Bin diameter_list into segments
        bins = np.linspace(min_diameter, max_diameter, segments+1)
        counts, _ = np.histogram(diameter_list, bins)
        percentages = (counts / len(diameter_list)) * 100
        plot_statistics(bins, 
                        percentages, 
                        segments, 
                        "Particle Diameter", 
                        "Diameter Range",
                        os.path.join(output_folder, "diameter.png"))

        # Bin nn_dist into segments
        bins_nn = np.linspace(min_nn_dist, max_nn_dist, segments+1)
        counts_nn, _ = np.histogram(nn_dist, bins_nn)
        percentages_nn = (counts_nn / len(nn_dist)) * 100
        plot_statistics(bins_nn,
                        percentages_nn,
                        segments,
                        "Distance Between Particle Centers",
                        "Nearest Neighbor Distance Range",
                        os.path.join(output_folder, "nn_dist.png"))

        # Bin r_nn_dist into segments
        bins_r_nn = np.linspace(min_r_nn_dist, max_r_nn_dist, segments+1)
        counts_r_nn, _ = np.histogram(r_nn_dist, bins_r_nn)
        percentages_r_nn = (counts_r_nn / len(r_nn_dist)) * 100
        plot_statistics(bins_r_nn,
                        percentages_r_nn, segments,
                        "Distance Between Particle Radii",
                        "Radius-Adjusted Distance Range",
                        os.path.join(output_folder, "r_nn_dist.png"))

        # Create the text file with statistics
        statistics_file_path = os.path.join(output_folder, 'particle_statistics.txt')
        with open(statistics_file_path, 'w') as f:
            # Particle statistics for diameter_list
            f.write(f"Number of particles: {len(diameter_list)}\n\n")
            f.write(f"Mean diameter: {mean_diameter:.4f}\n")
            f.write(f"Max diameter: {max_diameter:.4f}\n")
            f.write(f"Min diameter: {min_diameter:.4f}\n")
            f.write(f"Variance: {variance_diameter:.4f}\n")
            f.write(f"Standard Deviation: {std_deviation_diameter:.4f}\n\n")
            
            f.write("Particle diameter Distribution:\n")
            for i in range(segments):
                f.write(f"Segment {i+1} (Range: {bins[i]:.4f} to {bins[i+1]:.4f}): {counts[i]} particles ({percentages[i]:.2f}%)\n")
            
            f.write("\n-------------------------------------------------------\n")
            
            # Particle statistics for nn_dist
            f.write("\nDistance between particle center\n\n")
            f.write(f"Mean distance: {mean_nn_dist:.4f}\n")
            f.write(f"Max distance: {max_nn_dist:.4f}\n")
            f.write(f"Min distance: {min_nn_dist:.4f}\n")
            f.write(f"Variance distance: {variance_nn_dist:.4f}\n")
            f.write(f"Standard Deviation of distance: {std_deviation_nn_dist:.4f}\n\n")
            
            f.write("Distance Distribution:\n")
            for i in range(segments):
                f.write(f"Segment {i+1} (Range: {bins_nn[i]:.4f} to {bins_nn[i+1]:.4f}): {counts_nn[i]} particles ({percentages_nn[i]:.2f}%)\n")
            
            f.write("\n-------------------------------------------------------\n")
            
            # Particle statistics for r_nn_dist
            f.write("\nDistance between particle radii\n\n")
            f.write(f"Mean distance: {mean_r_nn_dist:.4f}\n")
            f.write(f"Max distance: {max_r_nn_dist:.4f}\n")
            f.write(f"Min distance: {min_r_nn_dist:.4f}\n")
            f.write(f"Variance distance: {variance_r_nn_dist:.4f}\n")
            f.write(f"Standard Deviation: {std_deviation_r_nn_dist:.4f}\n\n")
            
            f.write("Distance Distribution:\n")
            for i in range(segments):
                f.write(f"Segment {i+1} (Range: {bins_r_nn[i]:.4f} to {bins_r_nn[i+1]:.4f}): {counts_r_nn[i]} particles ({percentages_r_nn[i]:.2f}%)\n")
            
            
def convert_to_solid(vertices, faces):
    """Convert convex hulls to solids in CadQuery"""
    if len(faces) < 2:
        raise ValueError("More than one wire or face is required to create a solid.")

    face_list = []
    
    for simplex in faces:
        pts = [cq.Vector(*vertices[i]) for i in simplex]
        wire = cq.Wire.makePolygon(pts + [pts[0]])  # Ensure closed loop
        face = cq.Face.makeFromWires(wire)
        face_list.append(face)

    # Create a shell from faces and convert to solid
    shell = cq.Shell.makeShell(face_list)
    solid = cq.Solid.makeSolid(shell)
    
    return solid


def compute_cell_radius(cell, vor_vertices):
    """Compute the radius of the inscribed sphere inside a Voronoi cell"""
    cell_vertices = vor_vertices[cell]
    centroid = np.mean(cell_vertices, axis=0)

    hull = ConvexHull(cell_vertices)
    min_dist = np.inf
    for simplex in hull.simplices:
        p1, p2, p3 = hull.points[simplex[0]], hull.points[simplex[1]], hull.points[simplex[2]]
        v1, v2 = p2 - p1, p3 - p1
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        dist = abs(np.dot(centroid - p1, normal))
        min_dist = min(min_dist, dist)
    
    return centroid, min_dist


def generate_points_on_sphere(center, radius):
    """Function to generate points on the surface of a sphere"""
    points = []
    max_attempts = 100
    attempts = 0

    while attempts < max_attempts:
        theta = random.uniform(0, 2 * np.pi)
        phi = random.uniform(0, np.pi)

        x = center[0] + radius * np.sin(phi) * np.cos(theta)
        y = center[1] + radius * np.sin(phi) * np.sin(theta)
        z = center[2] + radius * np.cos(phi)

        if all(np.linalg.norm(np.array([x, y, z]) - np.array(p)) >= radius for p in points):
            points.append([x, y, z])
            attempts = 0
        else:
            attempts += 1

    return np.array(points)


def plot_statistics(bins, percentages, segments, title, xlabel, filename):
    plt.figure(figsize=(9, 6))
    plt.bar(range(1, segments+1), percentages, tick_label=[f"{bins[i]:.2f}-{bins[i+1]:.2f}" for i in range(segments)])
    plt.xlabel(xlabel)
    plt.ylabel("Percentage of Particles")
    plt.title(title)
    plt.xticks(rotation=90)
    plt.yticks()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename, format='png') 
    plt.close()
