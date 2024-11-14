# Graviton Particle Simulation

A visual simulation of particle motion influenced by gravity using gravitons, created in Python with Pygame. This simulation demonstrates a simple physics model in which particles interact with virtual "gravitons", creating a dynamic and visually engaging gravitational effect.

## Features

- **Particle Motion**: Particles are randomly generated with forces acting on them, simulating realistic motion.
- **Graviton Forces**: Gravitons are created around each particle and apply gravitational forces, influencing the motion of nearby particles.
- **Collision and Boundary Handling**: Particles respect screen boundaries and reverse direction when reaching edges.
- **Configurable Simulation**: Easily adjustable constants for particle count, graviton lifespan, screen resolution, and other settings to customize the simulation.

## Requirements

- **Python 3.x**
- **Pygame**: Install it via pip with `pip install pygame`

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/LoanTB/Simple-Graviton-Particle-Simulation.git
   cd Simple-Graviton-Particle-Simulation
   ```

2. Install Pygame if not already installed:
   ```bash
   pip install pygame
   ```

3. Run the simulation:
   ```bash
   python main.py
   ```

## Project Structure

- **`main.py`**: The main script for the simulation. It initializes the screen, creates particles and gravitons, and handles the simulation loop.
- **`Configuration` Class**: Contains constants for simulation settings, such as screen resolution, particle size, graviton lifespan, and more.
- **`Particle` Class**: Represents individual particles with position, forces, and color attributes. Handles movement and boundary collisions.
- **`Graviton` Class**: Represents gravitons, which influence particle motion by applying gravitational-like forces.

## Customization

All configuration constants are centralized in the `Configuration` class, allowing you to easily modify:

- **Screen Resolution** (`SCREEN_RESOLUTION`)
- **Particle Count** (`PARTICLE_COUNT`)
- **Graviton Count Per Particle** (`GRAVITON_CREATION_COUNT`)
- **Frame Rate** (`FRAME_RATE`)
- **Color, Size, and Force Constraints** for particles and gravitons

Adjust these constants in the `Configuration` class to see how changes impact the simulation dynamics.

## Simulation Details

The simulation creates an interaction between particles and gravitons:
- **Particles** move based on initial forces and can reverse direction upon hitting screen boundaries.
- **Gravitons** are generated around each particle, applying a small gravitational force on nearby particles. Gravitons have a short lifespan and fade over time, but they effectively influence particles, creating a visible "gravity" effect.

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0).

### Additional Note on Commercial Use
**Commercial use of this software or any derived works is prohibited without prior written permission from the original author.** For commercial licensing inquiries, please contact loan.tremoulet.breton@gmail.com.
