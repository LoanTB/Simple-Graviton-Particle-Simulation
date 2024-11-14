import pygame
import random
import math

class Configuration:
    """Configuration constants for the Particle and Graviton Simulation."""

    # Screen settings
    SCREEN_RESOLUTION = [700, 700]
    WINDOW_TITLE = "Particle and Graviton Simulation"
    FRAME_RATE = 30
    BACKGROUND_COLOR = (0, 0, 0)

    # Particle settings
    PARTICLE_COUNT = 3
    PARTICLE_SIZE = 10
    PARTICLE_SPAWN_OFFSET = 10
    PARTICLE_COLOR_MIN = 100
    PARTICLE_COLOR_RANGE = 155
    FORCE_LIMIT = 2

    # Graviton settings
    GRAVITON_SIZE = 1
    GRAVITON_LIFE = 100
    GRAVITON_CREATION_COUNT = 30
    GRAVITON_FORCE_ADDITION_RANGE = 10
    GRAVITON_FORCE_APPLY_MULTIPLIER = -0.01
    GRAVITON_COLOR_MULTIPLIER = 0.5

class Particle:
    """Represents a particle with position, forces, color, and size."""

    def __init__(self, forces, spawn_zone, size):
        """
        Initializes a Particle instance.

        Args:
            forces (list): Initial force vector [fx, fy].
            spawn_zone (list): Spawn area defined by [x_min, y_min, x_max, y_max].
            size (int): Radius of the particle.
        """
        self.position = [
            spawn_zone[0] + random.random() * (spawn_zone[2] - spawn_zone[0]),
            spawn_zone[1] + random.random() * (spawn_zone[3] - spawn_zone[1]),
        ]
        self.forces = forces
        self.color = [
            Configuration.PARTICLE_COLOR_MIN + random.randint(0, Configuration.PARTICLE_COLOR_RANGE),
            Configuration.PARTICLE_COLOR_MIN + random.randint(0, Configuration.PARTICLE_COLOR_RANGE),
            Configuration.PARTICLE_COLOR_MIN + random.randint(0, Configuration.PARTICLE_COLOR_RANGE),
        ]
        self.size = size

    def apply_force(self, force, limits):
        """
        Applies a force to the particle, reversing direction if limits are exceeded.

        Args:
            force (list): Force vector [fx, fy] to apply.
            limits (list): Boundary limits [width, height].
        """
        for i in range(2):
            projected_position = self.position[i] + self.forces[i] + force[i]
            if (projected_position - self.size < 0) or (projected_position + self.size > limits[i]):
                self.forces[i] *= -1
            self.forces[i] += force[i]

    def update(self, limits):
        """
        Updates the particle's position based on current forces and enforces boundary constraints.

        Args:
            limits (list): Boundary limits [width, height].
        """
        for i in range(2):
            self.forces[i] = max(min(self.forces[i], Configuration.FORCE_LIMIT), -Configuration.FORCE_LIMIT)
            projected_position = self.position[i] + self.forces[i]
            if (projected_position - self.size < 0) or (projected_position + self.size > limits[i]):
                self.forces[i] *= -1
            self.position[i] += self.forces[i]

    def draw(self, surface):
        """
        Renders the particle on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the particle on.
        """
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.position[0]), int(self.position[1])),
            self.size,
        )

class Graviton:
    """Represents a graviton with its own properties and a reference to its creator."""

    def __init__(self, creator, position, forces, size=Configuration.GRAVITON_SIZE, life=Configuration.GRAVITON_LIFE):
        """
        Initializes a Graviton instance.

        Args:
            creator (Particle): The particle that created this graviton.
            position (list): Initial position [x, y].
            forces (list): Initial force vector [fx, fy].
            size (int, optional): Radius of the graviton. Defaults to Configuration.GRAVITON_SIZE.
            life (int, optional): Lifespan of the graviton in frames. Defaults to Configuration.GRAVITON_LIFE.
        """
        self.creator = creator
        self.position = position.copy()
        self.forces = forces.copy()
        self.color = [
            creator.color[0] * Configuration.GRAVITON_COLOR_MULTIPLIER,
            creator.color[1] * Configuration.GRAVITON_COLOR_MULTIPLIER,
            creator.color[2] * Configuration.GRAVITON_COLOR_MULTIPLIER,
        ]
        self.size = size
        self.life = life

    def apply_force(self, force):
        """
        Applies a force to the graviton.

        Args:
            force (list): Force vector [fx, fy] to apply.
        """
        self.forces = [self.forces[i] + force[i] for i in range(2)]

    def update(self, limits):
        """
        Updates the graviton's position based on current forces.

        Args:
            limits (list): Boundary limits [width, height].
        """
        for i in range(2):
            self.position[i] += self.forces[i]

    def draw(self, surface):
        """
        Renders the graviton on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the graviton on.
        """
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.position[0]), int(self.position[1])),
            self.size,
        )

def main():
    """Main function to run the particle and graviton simulation."""
    pygame.init()
    clock = pygame.time.Clock()
    resolution = Configuration.SCREEN_RESOLUTION
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption(Configuration.WINDOW_TITLE)

    particles = [
        Particle(
            forces=[0, 0],
            spawn_zone=[
                Configuration.PARTICLE_SPAWN_OFFSET,
                Configuration.PARTICLE_SPAWN_OFFSET,
                resolution[0] - Configuration.PARTICLE_SPAWN_OFFSET,
                resolution[1] - Configuration.PARTICLE_SPAWN_OFFSET
            ],
            size=Configuration.PARTICLE_SIZE
        )
        for _ in range(Configuration.PARTICLE_COUNT)
    ]
    gravitons = []

    running = True
    while running:
        clock.tick(Configuration.FRAME_RATE)
        screen.fill(Configuration.BACKGROUND_COLOR)

        for particle in particles:
            particle.draw(screen)
            particle.update(resolution)
            for _ in range(Configuration.GRAVITON_CREATION_COUNT):
                graviton_position = particle.position.copy()
                graviton_forces = [
                    particle.forces[0] + (random.random() - 0.5) * Configuration.GRAVITON_FORCE_ADDITION_RANGE,
                    particle.forces[1] + (random.random() - 0.5) * Configuration.GRAVITON_FORCE_ADDITION_RANGE,
                ]
                gravitons.append(Graviton(particle, graviton_position, graviton_forces))

        for graviton in gravitons[:]:
            graviton.draw(screen)
            graviton.update(resolution)
            graviton.life -= 1
            if (
                graviton.life <= 0
                or graviton.position[0] < 0
                or graviton.position[0] > resolution[0]
                or graviton.position[1] < 0
                or graviton.position[1] > resolution[1]
            ):
                gravitons.remove(graviton)
                continue

            for particle in particles:
                if particle is graviton.creator:
                    continue
                dx = graviton.position[0] - particle.position[0]
                dy = graviton.position[1] - particle.position[1]
                distance = math.hypot(dx, dy)
                if distance < particle.size + graviton.size:
                    particle.apply_force([
                        graviton.forces[0] * Configuration.GRAVITON_FORCE_APPLY_MULTIPLIER,
                        graviton.forces[1] * Configuration.GRAVITON_FORCE_APPLY_MULTIPLIER,
                    ], resolution)
                    gravitons.remove(graviton)
                    break

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
