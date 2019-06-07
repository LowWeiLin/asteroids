import sys, pygame
import time
import numpy as np
from AsteroidsGame import AsteroidsGame


black = (0, 0, 0)
white = (255, 255, 255)


class Renderer:
    def __init__(self):
        self.game = AsteroidsGame()

        pygame.init()
        self.screen = pygame.display.set_mode(self.game.borders)

    def render_objects(self):
        for i, object_type in enumerate(self.game.object_type):
            if object_type == "player":
                self.render_player(i)
            if object_type == "asteroid":
                self.render_asteroid(i)
            if object_type == "bullet":
                self.render_bullet(i)

    def render_player(self, i):
        radius = self.game.object_radius[i]
        rot = np.radians(self.game.object_rotation[i])
        pos = np.array(self.game.object_position[i])
        vec1 = pos + np.array([0, radius])
        vec2 = pos + np.array([radius / 2, -radius])
        vec3 = pos + np.array([-radius / 2, -radius])
        points = np.array([vec1, vec2, vec3])
        points -= pos
        c, s = np.cos(rot), np.sin(rot)
        j = np.matrix([[c, s], [-s, c]])
        points = np.dot(j, points.T).T
        points += pos
        points = points.astype(int).tolist()
        pygame.draw.lines(self.screen, white, True, points, 1)

    def render_asteroid(self, i):
        radius = self.game.object_radius[i]
        pos = np.array(self.game.object_position[i]).astype(int)
        pygame.draw.circle(self.screen, white, pos, radius, 1)

    def render_bullet(self, i):
        radius = self.game.object_radius[i]
        pos = np.array(self.game.object_position[i]).astype(int)
        pygame.draw.circle(self.screen, white, pos, radius, 1)

    def gameloop(self):
        while True:
            player_actions = {}
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    sys.exit()

            # Get actions
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
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
            self.screen.fill(black)
            self.render_objects()
            pygame.display.flip()

            # Sleep
            time.sleep(0.1)


if __name__ == "__main__":
    renderer = Renderer()
    renderer.gameloop()
