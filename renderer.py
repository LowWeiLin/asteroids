"""
Renderer to render asteroids game using pygame
"""

import sys
import time
import pygame
import numpy as np
from asteroids_game import AsteroidsGame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Renderer:
    """
    Renderer to render asteroids game using pygame
    """

    def __init__(self):
        self.game = AsteroidsGame()

        pygame.init()
        self.screen = pygame.display.set_mode(self.game.borders)

    def render_objects(self):
        """
        Renders all objects
        """
        for i, object_type in enumerate(self.game.object_type):
            if object_type == "player":
                self.render_player(i)
            if object_type == "asteroid":
                self.render_asteroid(i)
            if object_type == "bullet":
                self.render_bullet(i)

    def render_player(self, i):
        """
        Renders a player
        """
        radius = self.game.object_radius[i]
        rot = np.radians(self.game.object_rotation[i])
        pos = np.array(self.game.object_position[i])
        vec1 = pos + np.array([0, radius])
        vec2 = pos + np.array([radius / 2, -radius])
        vec3 = pos + np.array([-radius / 2, -radius])
        points = np.array([vec1, vec2, vec3])
        points -= pos
        cos, sin = np.cos(rot), np.sin(rot)
        rot_mat = np.matrix([[cos, sin], [-sin, cos]])
        points = np.dot(rot_mat, points.T).T
        points += pos
        points = points.astype(int).tolist()
        pygame.draw.lines(self.screen, WHITE, True, points, 1)

    def render_asteroid(self, i):
        """
        Renders an asteroid
        """
        radius = self.game.object_radius[i]
        pos = np.array(self.game.object_position[i]).astype(int)
        pygame.draw.circle(self.screen, WHITE, pos, radius, 1)

    def render_bullet(self, i):
        """
        Renders a bullet
        """
        radius = self.game.object_radius[i]
        pos = np.array(self.game.object_position[i]).astype(int)
        pygame.draw.circle(self.screen, WHITE, pos, radius, 1)

    def gameloop(self):
        """
        Game loop
        """
        while True:
            player_actions = {}
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    sys.exit()

            # Get actions
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_actions["rotate_left"] = True
            if keys[pygame.K_RIGHT]:
                player_actions["rotate_right"] = True
            if keys[pygame.K_UP]:
                player_actions["accelerate_forward"] = True
            if keys[pygame.K_SPACE]:
                player_actions["shoot"] = True

            # Step
            actions = [player_actions]
            self.game.step(actions)

            # Render
            self.screen.fill(BLACK)
            self.render_objects()
            pygame.display.flip()

            # Sleep
            time.sleep(0.1)


if __name__ == "__main__":
    RENDERER = Renderer()
    RENDERER.gameloop()
