# Typing game
import pygame


def main():

    pygame.init()

    pygame.display.set_mode((500, 750))
    pygame.display.set_caption("CowType")

    w_surface = pygame.display.get_surface()
    game = Game(w_surface)
    game.play()

    pygame.quit()


class Game:
    def __init__(self, surface):
        self.surface = surface
        self.bg_color = pygame.Color("black")
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

    def play(self):
        # plays the game
        while not self.close_clicked:

            # play frame
            self.handle_events()
            self.draw()
            if self.continue_game:
                pass

            self.game_Clock.tick(self.FPS)  # run at most with FPS

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True

    def draw(self):
        # draw the image onto screen
        self.surface.fill(self.bg_color)

        self.draw_intro()

        pygame.display.update()

    def draw_intro(self):
        image = pygame.image.load("./type-speed-open.png")
        image_width = self.surface.get_width()
        image_height = self.surface.get_height()
        image = pygame.transform.scale(image, (image_width, image_height))
        self.surface.blit(image, (0, 0))


if __name__ == "__main__":
    main()
