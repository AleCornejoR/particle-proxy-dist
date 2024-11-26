import csv
import random
import json


def load_config(config_path):
    """
    Load the configuration from a JSON file.

    :param config_path: Path to the config JSON file.
    :return: Parsed configuration as a dictionary.
    """
    with open(config_path, mode="r") as file:
        return json.load(file)


def generate_random_particles(file_path, num_particles, x_range, y_range):
    """
    Generate random particles with X, Y coordinates within specified ranges and save them to a CSV file.

    :param file_path: Path to the CSV file where the particles will be saved.
    :param num_particles: Number of random particles to generate.
    :param x_range: Tuple defining the min and max limits for X coordinates (min_x, max_x).
    :param y_range: Tuple defining the min and max limits for Y coordinates (min_y, max_y).
    """
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])  # CSV header
        for _ in range(num_particles):
            x = random.uniform(x_range[0], x_range[1])
            y = random.uniform(y_range[0], y_range[1])
            writer.writerow([x, y])
    print(
        f"[*] Generated {num_particles} random particles within X:{x_range} and Y:{y_range}, saved to {file_path}."
    )


def main():
    # Load configuration
    config = load_config("modules/config/config.json")
    particle_config = config["particle_generator"]

    # Set random seed for reproducibility
    random.seed(particle_config["random_seed"])

    # Generate particles based on config
    for size, file_path in particle_config["output_files"].items():
        num_particles = particle_config["num_particles"][size]
        x_range = particle_config["x_range"]
        y_range = particle_config["y_range"]
        generate_random_particles(file_path, num_particles, x_range, y_range)


if __name__ == "__main__":
    main()
