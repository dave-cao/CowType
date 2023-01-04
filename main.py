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
        self.start_timer = False

        # user input
        # self.user_text = ""
        # self.new_line = ""
        self.input_offset = self.surface.get_height() // 2
        self.input_x = 100
        self.input_list = [Input(self.input_x, self.input_offset, self.surface)]

    def play(self):
        # plays the game
        while not self.close_clicked:

            # play frame
            self.handle_events()
            self.draw()

            # Start the timer when a key is pressed
            if self.start_timer:
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
                self.check_newline()
                self.handle_keydown(event)
                # start the timer when a key is pressed
                if not self.start_timer:
                    self.start_timer = True

    def handle_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.handle_backspace(event)

        else:
            self.input_list[-1].update_content(event.unicode)

    def handle_backspace(self, event):
        # handles the backspace event
        if self.input_list[0].get_content() != " ":
            self.input_list[-1].delete_char()
        if not self.input_list[-1].get_content() and self.input_list[0].get_content():
            self.input_list.pop()

    def check_newline(self):
        end_of_type_screen = 200
        for user_input in self.input_list:
            if (
                user_input.get_width() > self.surface.get_width() - end_of_type_screen
                and user_input.check_on()
            ):
                self.input_offset += 80
                self.input_list.append(
                    Input(self.input_x, self.input_offset, self.surface)
                )

                self.update_lines(user_input)

    def update_lines(self, user_input):
        # updates the new lines with the word of the previous line and
        # updates the previous line without the word of the next line

        # get the last word of current input and give to next input
        # update the content of the most recent input with the last word
        # of previous input (current)
        current_last_word = user_input.get_content().split()[-1]
        without_last_word = " ".join(user_input.get_content().split()[:-1])
        # set the current userinput to delete the last word
        original_input = user_input.get_content()
        user_input.set_content(without_last_word)

        # if the user_input is blank, then don't do this
        if user_input.get_content():
            self.input_list[-1].update_content(current_last_word)

            # Makes it so we do not update the old lines
            user_input.switch_on_to_off()

        else:
            # if the user content is blank
            user_input.set_content(original_input)
            user_input.switch_on_to_off()

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

        # self.draw_inputbox()
        # if not self.continue_game:
        #     self.draw_new_line()

        for user_input in self.input_list:
            user_input.draw_content()

        pygame.display.update()

    def draw_intro(self):
        image = pygame.image.load("./type-speed-open.png")
        image_width = self.surface.get_width()
        image_height = self.surface.get_height()
        image = pygame.transform.scale(image, (image_width, image_height))
        self.surface.blit(image, (0, 0))


class Input:
    def __init__(self, x, y, surface):
        width = 30
        height = 50
        self.x = x
        self.y = y

        self.font = pygame.font.Font("./font/Andika-Regular.ttf", 30)
        self.rect = pygame.Rect(x, y, width, height)

        self.surface = surface
        self.color_active = pygame.Color("#665c54")
        self.color_passive = pygame.Color("#ebdbb2")
        self.bg_color = pygame.Color("#262626")

        self.content = ""

        self.on = True

    def draw_content(self):

        # input

        # blit the text box
        text_box = self.font.render(self.content, True, self.color_active)
        location = self.rect.x + 5, self.rect.y

        # draw the rect
        self.rect.width = text_box.get_width() + 10
        pygame.draw.rect(self.surface, self.color_passive, self.rect)

        # blit the text after so it shows up first
        self.surface.blit(text_box, location)

    def update_content(self, letter):
        self.content += letter

    def delete_char(self):
        self.content = self.content[:-1]

    def get_width(self):
        return self.rect.width

    def check_on(self):
        return self.on

    def switch_on_to_off(self):
        self.on = False

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content


if __name__ == "__main__":
    main()
