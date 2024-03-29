"""
Asteroids game
"""

import numpy as np
from scipy.spatial import distance


class AsteroidsGame:
    """
    Asteroids game
    """

    def __init__(self):
        # Configs
        self.borders = np.array((800, 800))  # Screen wraps around at borders
        self.asteroids_speed = 5
        self.asteroids_max_radius = 80
        self.asteroids_min_radius = 20
        self.asteroids_split_radius_ratio = 0.5

        self.bullet_radius = 5
        self.bullet_speed = 10
        self.bullet_lifespan = 50

        self.player_radius = 10
        self.player_acceleration = 0.5
        self.player_rotation_speed = 15
        self.player_max_speed = 7
        self.player_bullet_cooldown = 20

        # State
        self.steps = 0

        self.object_position = []
        self.object_velocity = []
        self.object_radius = []
        self.object_rotation = []
        self.object_type = []
        self.object_steps = []

        self.player_alive = []
        self.player_cooldown = []

        # Initialize
        self.add_player()
        for _ in range(4):
            self.add_asteroid()

    def move_all(self):
        """
        Moves all entities
        """
        self.object_position = (
            (np.array(self.object_position) + np.array(self.object_velocity))
            % self.borders
        ).tolist()

    def add_player(self, position=None):
        """
        Add a player
        """
        self.object_position.append(
            position if position else np.random.rand(2) * self.borders
        )
        self.object_velocity.append(np.zeros(2))
        self.object_radius.append(self.player_radius)
        self.object_rotation.append(0 * np.random.rand() * 360)
        self.object_type.append("player")
        self.object_steps.append(0)

        self.player_alive.append(1)
        self.player_cooldown.append(0)

    def add_asteroid(self, radius=None, position=None, velocity=None):
        """
        Adds an asteroid
        """
        self.object_position.append(
            position if position else np.random.rand(2) * self.borders
        )
        self.object_velocity.append(
            velocity if velocity else np.random.rand(2) * self.asteroids_speed
        )
        self.object_radius.append(radius if radius else self.asteroids_max_radius)
        self.object_rotation.append(0)
        self.object_type.append("asteroid")
        self.object_steps.append(0)

    def add_bullet(self, position, velocity):
        """
        Adds a bullet
        """
        self.object_position.append(position)
        self.object_velocity.append(velocity)
        self.object_radius.append(self.bullet_radius)
        self.object_rotation.append(0)
        self.object_type.append("bullet")
        self.object_steps.append(0)

    def remove_bullets(self):
        """
        Removes bullets that exceeds their lifespan
        """
        bullet_indexes_to_remove = [
            i
            for i, t in enumerate(self.object_type)
            if t == "bullet" and self.object_steps[i] > self.bullet_lifespan
        ]
        self.remove_objects(bullet_indexes_to_remove)

    def remove_objects(self, indexes):
        """
        Removes objects by indexes
        """
        fields = [
            "object_position",
            "object_velocity",
            "object_radius",
            "object_rotation",
            "object_type",
            "object_steps",
        ]
        for field in fields:
            setattr(
                self,
                field,
                [x for i, x in enumerate(getattr(self, field)) if i not in indexes],
            )

    def apply_actions(self, actions):
        """
        Applies actions
        """
        player_object_indexes = [
            i for i, t in enumerate(self.object_type) if t == "player"
        ]
        for player_index, player_actions in enumerate(actions):
            if not self.player_alive[player_index]:
                continue
            idx = player_object_indexes[player_index]
            for action, value in player_actions.items():
                if action == "rotate_left" and value:
                    self.object_rotation[idx] += self.player_rotation_speed
                    self.object_rotation[idx] %= 360
                if action == "rotate_right" and value:
                    self.object_rotation[idx] -= self.player_rotation_speed
                    self.object_rotation[idx] %= 360
                if action == "accelerate_forward" and value:
                    rot = np.radians(self.object_rotation[idx])
                    self.object_velocity[idx] += self.player_acceleration * np.array(
                        [np.sin(rot), np.cos(rot)]
                    )
                    speed = np.linalg.norm(self.object_velocity[idx])
                    if speed > self.player_max_speed:
                        self.object_velocity[idx] = (
                            self.object_velocity[idx] / speed * self.player_max_speed
                        )
                if action == "shoot" and value:
                    if self.player_cooldown[player_index] == 0:
                        rot = np.radians(self.object_rotation[idx])
                        self.add_bullet(
                            self.object_position[idx],
                            self.bullet_speed * np.array([np.sin(rot), np.cos(rot)]),
                        )
                        self.player_cooldown[player_index] = self.player_bullet_cooldown

    def step(self, actions):
        """
        Perform a game step
        """
        # Check alive
        if not True:
            return

        # Step
        self.steps += 1
        self.object_steps = (np.array(self.object_steps) + 1).tolist()
        self.player_cooldown = (np.array(self.player_cooldown) - 1).clip(0).tolist()

        # Apply actions
        self.apply_actions(actions)

        # Move objects
        self.move_all()
        self.remove_bullets()

        # Check collisions
        self.collide()

    def collide(self):
        """
        Checks and apply effects of collisions
        """
        dist = distance.cdist(self.object_position, self.object_position, "euclidean")
        collision = ((dist - self.object_radius) <= 0) * 1
        np.fill_diagonal(collision, 0)
        collision = np.sum(collision, axis=1)
        print(dist)
        print(collision)
        return collision


if __name__ == "__main__":
    print("hello")

    GAME = AsteroidsGame()
    for _ in range(1):
        GAME.step({})
