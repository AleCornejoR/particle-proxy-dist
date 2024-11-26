# Particle Analysis Project

This project is a Python-based application designed to analyze particles in an image. It includes functionalities for particle detection, visualization, and calculation of metrics such as the closest pair of particles. Additionally, the application now supports generating a mesh of triangles between detected particles using Delaunay triangulation.

---

## Features

- **Particle Detection:** Detect particles using contours and centroids.
- **Visualization:** 
  - Plot all detected particles and their centroids.
  - Highlight the closest pair of particles and draw a line between them (optional).
  - Generate and visualize a mesh of triangles connecting all particles (optional).
- **Metrics Calculation:** Find the closest pair of particles based on their distances.
- **Extensibility:** Modular design with `Particle` and `ParticleCalculator` classes for easy integration into other projects.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AleCornejoR/particle-proxy-dist.git
   cd particle-proxy-dist
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the main script**:  
   Ensure your input images are configured in the `sample_paths` list. Additionally, set up a reference image to calculate the scale. Then run:
   ```bash
   python main.py
   ```

2. **Modules**:  
   - `ImageProcessor`: Detects particles, applies preprocessing, and calculates their centroids.
   - `ParticleCalculator`: Analyzes the detected particles, provides metrics, and generates visualizations.

3. **Key Features**:
   - Detect particles from sample images.
   - Calculate and highlight the closest pair of particles.
   - Visualize a triangulated mesh of particles using Delaunay triangulation.

4. **Important**:  
   Before processing any sample images, you must create an instance for the reference image. The reference image is used to calculate the scale for accurate measurements. Here’s an example of how to process the reference:

   ```python
   # Process reference image
   reference_path = "data/reference.png"
   processor_ref = ImageProcessor(reference_path)

   # Calculate the scale, with optional visualization of intermediate steps
   processor_ref.calculate_scale(
       real_length=200,       # Real-world length of the reference bar (e.g., in micrometers)
       show_original=False,   # Show original image (optional)
       show_binary=False,     # Show binary version (optional)
       show_contours=False,   # Show contours (optional)
       show_bar=False         # Show reference bar detection (optional)
   )
   ```
   The calculated scale is then used to process subsequent sample images for consistent and accurate distance measurements.


---

## Example

Below is an example of how to process and visualize particles:

```python
from modules.classes import ImageProcessor, ParticleCalculator

# Process the reference image to calculate the scale
reference_path = "data/reference.png"
processor_ref = ImageProcessor(reference_path)
processor_ref.calculate_scale(real_length=200)

# Process a sample image
image_path = "data/sample1.png"
processor = ImageProcessor(image_path)
processor.scale = processor_ref.scale  # Use the calculated scale
processor.obtain_particles()

# Analyze detected particles
calculator = ParticleCalculator(processor.particles)
calculator.find_closest_pair()

# Plot particles with the closest pair highlighted and the triangulated mesh
calculator.plot_particles(show_closest=True, show_mesh=True)
```


---

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

*Developed by Rafael Cornejo.*

Email: rafael.cornejo.rdz@gmail.com
