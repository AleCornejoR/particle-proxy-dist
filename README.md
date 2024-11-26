# Particle Analysis Project

This project is a Python-based application designed to analyze particles in an image. It includes functionalities for particle detection, visualization, and calculation of metrics such as the closest pair of particles.

---

## Features

- **Particle Detection:** Detect particles using contours and centroids.
- **Visualization:** 
  - Plot all detected particles and their centroids.
  - Highlight the closest pair of particles and draw a line between them (optional).
- **Metrics Calculation:** Find the closest pair of particles based on their distances.
- **Extensibility:** Modular design with `Particle` and `ParticleCalculator` classes for easy integration into other projects.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AleCornejoR/particle-proximity-distribution.git
   cd particle-proximity-distribution
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the main script**:  
   Ensure your input image is available and configured in the script. Run the following:
   ```bash
   python main.py
   ```

2. **Modules**:  
   - `ImageProcessor`: Detects particles and calculates their centroids.
   - `ParticleCalculator`: Analyzes the detected particles and provides metrics and plots.

---

## Example

Below is an example of how to visualize the detected particles and their centroids:

```python
from modules.classes.ParticleCalculator import ParticleCalculator

# Assuming particles have been detected using ImageProcessor
particle_calculator = ParticleCalculator(particles)

# Plot the particles
particle_calculator.plot_particles(show_closest=True)

# Find and display the closest pair
particle_calculator.find_closest_pair()
print(particle_calculator.closest_pair)
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
