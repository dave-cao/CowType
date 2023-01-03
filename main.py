# Typing game
import pygame


def main():

    pygame.init()

    pygame.display.set_mode((800, 750))
    pygame.display.set_caption("CowType")

    w_surface = pygame.display.get_surface()
    game = Game(w_surface)
    game.play()

    pygame.quit()


class Game:
    def __init__(self, surface):
        self.surface = surface
        self.bg_color = pygame.Color("#262626")
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # Keeping track of time
        self.time = 0
        self.second = 0

        # user input
        self.user_text = ""

    def play(self):
        # plays the game
        while not self.close_clicked:

            # play frame
            self.handle_events()
            self.draw()
            self.track_time()
            if self.continue_game:
                pass

            self.game_Clock.tick(self.FPS)  # run at most with FPS

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True

            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.user_text = self.user_text[:-1]

        else:
            self.user_text += event.unicode

    def track_time(self):
        self.time += 1
        if not self.time % 60:
            self.second += 1

    def draw(self):
        # draw the image onto screen
        self.surface.fill(self.bg_color)

        # We only want to draw the intro for a few seconds
        # if self.second < 2:
        #    self.draw_intro()

        self.draw_inputbox()

        pygame.display.update()

    def draw_intro(self):
        image = pygame.image.load("./type-speed-open.png")
        image_width = self.surface.get_width()
        image_height = self.surface.get_height()
        image = pygame.transform.scale(image, (image_width, image_height))
        self.surface.blit(image, (0, 0))

    def draw_inputbox(self):

        font = pygame.font.SysFont("", 30)
        input_rect = pygame.Rect(200, 200, 500, 32)
        color_active = pygame.Color("#665c54")
        color_passive = pygame.Color("#ebdbb2")
        color = color_passive

        x = self.surface.get_width() // 2 - input_rect.width // 2
        y = self.surface.get_height() - 200
        input_rect.x = x
        input_rect.y = y

        text_box = font.render(self.user_text, True, color_active)

        location = input_rect.x + 5, input_rect.y + 5

        input_rect.w = max(input_rect.w, text_box.get_width() + 10)
        pygame.draw.rect(self.surface, color_passive, input_rect)
        self.surface.blit(text_box, location)


if __name__ == "__main__":
    main()
