# Typing game
import random

import pygame


def main():

    # Starts pygame and sets screen
    pygame.init()
    pygame.display.set_mode((800, 750))
    pygame.display.set_caption("CowType")

    w_surface = pygame.display.get_surface()

    # initialize game class and begin game
    game = Game(w_surface)
    game.play()

    pygame.quit()


class Game:
    def __init__(self, surface):
        """The Game class contains the functionality of the typing game

        surface(pygame.display): the display surface of pygame
        """
        # General variables
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

        # Input variables
        self.input_offset = self.surface.get_height() // 2
        self.input_x = 20
        self.input_list = [Input(self.input_x, self.input_offset, self.surface)]
        self.raw_text = ""
        self.sentence = self.get_sentence()

        # text color and font
        self.color_active = pygame.Color("#ebdbb2")
        self.color_passive = pygame.Color("#665c54")
        self.font = pygame.font.Font("./font/Andika-Regular.ttf", 30)

        # calculating WPM and acc
        self.total_keys_pressed = 0
        self.WPM = 0
        self.raw_wpm = 0
        self.accuracy = 0

    def get_sentence(self):
        """Gets a random sentence from txt file
        Returns:
            random_sentence(str): a string of the random sentence taken
        """
        with open("./sentences.txt", "r") as file:
            sentences = file.readlines()

        random_sentence = random.choice(sentences)
        return random_sentence

    def blit_text(self, text, pos, font):
        """Wraps the sentence/text given within the surface width."""
        words = [
            word.split(" ") for word in text.splitlines()
        ]  # 2D array where each row is a list of words.
        space = font.size(" ")[0]  # The width of a space.
        max_width = self.surface.get_size()[0]
        x, y = pos
        word_height = 0
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, self.color_passive)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def draw_sentence(self):
        """Draws the random sentence onto the screen"""
        self.blit_text(self.sentence, (20, 20), self.font)

    def play(self):
        """Plays the game. Draws, handles all events, and tracks the time"""
        while not self.close_clicked:

            # play frame
            self.draw()
            self.handle_events()

            # Start the timer when a key is pressed
            if self.start_timer:
                self.track_time()

            self.game_Clock.tick(self.FPS)  # run at most with FPS

    def handle_events(self):
        """Handles all events of the game.
        This includes key presses and clicking QUIT"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True

            if self.continue_game:
                if event.type == pygame.KEYDOWN:
                    self.check_newline()
                    self.handle_keydown(event)
                    # start the timer when a key is pressed
                    if not self.start_timer:
                        self.start_timer = True

            else:
                if event.type == pygame.KEYDOWN:
                    # If the game is finished, press enter again to restart the game
                    self.restart_game(event)

    def restart_game(self, event):
        """Restarts the game"""
        if event.key == pygame.K_RETURN:
            # Keeping track of time
            self.time = 0
            self.second = 0
            self.start_timer = False

            # Input variables
            self.input_offset = self.surface.get_height() // 2
            self.input_x = 20
            self.input_list = [Input(self.input_x, self.input_offset, self.surface)]
            self.raw_text = ""
            self.sentence = self.get_sentence()

            # calculating WPM and acc
            self.total_keys_pressed = 0
            self.WPM = 0
            self.raw_wpm = 0
            self.accuracy = 0

            self.continue_game = True

    def handle_keydown(self, event):
        """Handles when user presses a key.
        Args:
            event(pygame.event): a key press event
        """
        if event.key == pygame.K_BACKSPACE:
            self.handle_backspace(event)
            self.check_wrong_char()

        elif event.key == pygame.K_RETURN:
            self.handle_enter(event)
        # makes sure that shift doesn't count towards key presses
        elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
            print("", end="")
        else:
            self.input_list[-1].update_content(event.unicode)
            self.raw_text += event.unicode
            self.total_keys_pressed += 1
            self.check_wrong_char()

    def handle_enter(self, event):
        """Handles when the user presses enter.
        When the user presses enter, the game ends, timer stops, and WPM / acc are
        calculated.
        """
        self.start_timer = False
        self.continue_game = False
        self.update_wpm()
        self.accuracy = self.get_accuracy()
        print(self.WPM, " AVERAGE WPM")
        print(round(self.get_wpm()), " RAW WPM")
        print(round(self.get_accuracy() * 100), " ACCURACY")

    def handle_backspace(self, event):
        """Handles the backspace event.

        Args:
            event(pygame.event): when the user presses backspace
        """
        if self.input_list[0].get_content() != " ":
            # what is shown to the user
            self.input_list[-1].delete_char()

            # used to calculate the wpm/acc
            self.raw_text = self.raw_text[:-1]

        # If there is no content in the current line, go to the previous one
        # make sure that the previous line exists
        if not self.input_list[-1].get_content() and self.input_list[0].get_content():
            self.input_list.pop()
            self.input_list[-1].turn_on_cursor()
            self.input_list[-1].switch_off_to_on()
            self.input_offset -= 50

    def check_wrong_char(self):
        """Checks if a wrong character is pressed. If so, then give colour warning"""
        try:
            for i, char in enumerate(self.raw_text):
                if char == self.sentence[i]:
                    for _list in self.input_list:
                        _list.set_correct()

            for i, char in enumerate(self.raw_text):
                if char != self.sentence[i]:
                    for _list in self.input_list:
                        _list.set_incorrect()

        except IndexError:
            print("Too many characters")

    def check_newline(self):
        """Checks to see if a new line needs to be created with user input.
        If so, go to a new line.
        """
        end_of_type_screen = 20
        for user_input in self.input_list:
            if (
                user_input.get_width() > self.surface.get_width() - end_of_type_screen
                and user_input.check_on()
            ):
                # turns off the cursor
                user_input.turn_off_cursor()
                self.input_offset += 50
                self.input_list.append(
                    Input(self.input_x, self.input_offset, self.surface)
                )

                self.update_lines(user_input)

    def update_lines(self, user_input):
        """
        Updates the new line with the last word of the previous line and
        updates the previous line without the word of the next line.

        """
        current_last_word = user_input.get_content().split(" ")[-1]
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
        """Begin tracking seconds once user starts typing"""
        self.time += 1
        if not self.time % 60:
            self.second += 1

    def draw(self):
        """Draw all content to the screen"""
        self.surface.fill(self.bg_color)

        # Draw what the user types
        for user_input in self.input_list:
            user_input.draw_content()

        # if the game is over, draw the score and restart prompt
        if not self.continue_game:
            self.draw_score()
            self.draw_continue()
        self.draw_sentence()

        pygame.display.update()

    def draw_continue(self):
        """Draws the restart prompt."""
        string = "Press Enter to restart"
        text_box = self.font.render(string, True, pygame.Color("#665c54"))

        x = self.surface.get_width() // 2 - text_box.get_width() // 2
        y = self.surface.get_height() // 2 - text_box.get_height() // 2 - 50
        location = x, y
        self.surface.blit(text_box, location)

    def draw_score(self):
        """Draws the WPM, acc, and raw WPM to the screen."""
        string = f"WPM: {self.WPM} | Acc: {round(self.accuracy * 100)}% | Raw: {self.raw_wpm}"
        text_box = self.font.render(string, True, pygame.Color("#ff8035"))

        x = self.surface.get_width() // 2 - text_box.get_width() // 2
        y = self.surface.get_height() - 100

        location = (x, y)
        self.surface.blit(text_box, location)

    def get_wpm(self):
        """Gets the raw wpm of the user.
        Returns:
            WPM(float): the raw WPM of the user.
        """
        minute = self.second / 60
        WPM = (self.total_keys_pressed / 5) / minute
        return WPM

    def get_accuracy(self):
        """Gets the accuracy of the user.
        Returns:
            accuracy(float): the accuracy in decimal of the user
        """
        sentence = self.raw_text
        correct = 0

        # If the user types more than what they are supposed to
        try:
            for i, char in enumerate(sentence):
                if char == self.sentence[i]:
                    correct += 1
        except IndexError:
            print("Went over")

        return correct / self.total_keys_pressed

    def update_wpm(self):
        """Updates the WPM and raw WPM to the game class"""
        average_wpm = self.get_wpm() * self.get_accuracy()
        self.WPM = round(average_wpm)
        self.raw_wpm = round(self.get_wpm())


class Input:
    def __init__(self, x, y, surface):
        """The input class is each line typed and displayed to the user."""
        width = 30
        height = 50
        self.x = x
        self.y = y

        self.font = pygame.font.Font("./font/Andika-Regular.ttf", 30)
        self.rect = pygame.Rect(x, y, width, height)
        self.cursor = pygame.Rect(x, y, 10, height)

        self.surface = surface
        self.color_active = pygame.Color("#ebdbb2")
        self.color_passive = pygame.Color("#665c54")
        self.bg_color = pygame.Color("#262626")

        self.content = ""

        # switches
        self.on = True
        self.end_of_line = False

    def draw_content(self):
        """Draws what the user typed onto the screen, and also a cursor."""

        # blit the text box
        text_box = self.font.render(self.content, True, self.color_active)
        location = self.rect.x + 5, self.rect.y

        # draw the rect
        self.rect.width = text_box.get_width() + 10
        pygame.draw.rect(self.surface, self.bg_color, self.rect)

        # draw a cursor
        if not self.end_of_line:
            self.cursor.x = self.rect.width + 16
            pygame.draw.rect(self.surface, self.color_passive, self.cursor)

        # blit the text after so it shows up first
        self.surface.blit(text_box, location)

    def update_content(self, letter):
        """Update the content of the input
        Args:
            letter(str): the letter that is being added to the content

        """

        self.content += letter

    def delete_char(self):
        """Deletes a character of the content"""
        self.content = self.content[:-1]

    def get_width(self):
        """Grabs the width of the input box"""
        return self.rect.width

    def check_on(self):
        """Checks to see if input line is the one being updated. True means yes, False
        means no."""
        return self.on

    def switch_on_to_off(self):
        """Tell the user that the line is no longer being updated."""
        self.on = False

    def switch_off_to_on(self):
        """Tells the user that the line is now being updated."""
        self.on = True

    def get_content(self):
        """Gets the content of the line."""
        return self.content

    def set_content(self, content):
        """Sets the content of the line."""
        self.content = content

    def turn_off_cursor(self):
        """Makes the cursor dissapear."""
        self.end_of_line = True

    def turn_on_cursor(self):
        """Makes the cursor appear."""
        self.end_of_line = False

    def set_incorrect(self):
        """Sets the line color to red"""
        self.color_active = pygame.Color("#cc241d")

    def set_correct(self):
        """Sets the line color back to normal"""
        self.color_active = pygame.Color("#ebdbb2")


if __name__ == "__main__":
    main()
