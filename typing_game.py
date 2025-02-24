import pygame
import random
import time

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 40
LETTER_SPACING = 5

# Initialize Pygame
pygame.init()
letterFont = pygame.font.SysFont('Rockwell', FONT_SIZE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Word:
    def __init__(self):
        self.word = random.choice(bip39_words).strip()
        self.index = 0

    def render(self):
        total_width = (FONT_SIZE + LETTER_SPACING) * len(self.word) - LETTER_SPACING
        x_offset = (SCREEN_WIDTH - total_width) // 2
        y_offset = SCREEN_HEIGHT // 2 - FONT_SIZE // 2

        for i, char in enumerate(self.word):
            color = YELLOW if i < self.index else RED
            char_surface = letterFont.render(char, True, color)
            screen.blit(char_surface, (x_offset + i * (FONT_SIZE + LETTER_SPACING), y_offset))

def display_score_and_timer(score, timer):
    score_surface = letterFont.render(f'Score: {score}', True, WHITE)
    timer_surface = letterFont.render(f'Time: {timer}', True, WHITE)
    screen.blit(score_surface, (10, SCREEN_HEIGHT - 40))
    screen.blit(timer_surface, (SCREEN_WIDTH - timer_surface.get_width() - 10, SCREEN_HEIGHT - 40))

def welcome_screen():
    input_active = True
    user_input = ""

    while input_active:
        screen.fill(BLACK)

        # Display welcome text and prompt for duration
        welcome_text = letterFont.render("Welcome to Typing Game!", True, WHITE)
        prompt_text = letterFont.render("Enter duration in minutes:", True, WHITE)
        user_input_text = letterFont.render(user_input + "_", True, WHITE)

        screen.blit(welcome_text, (SCREEN_WIDTH / 2 - welcome_text.get_width() / 2,
                                   SCREEN_HEIGHT / 2 - FONT_SIZE * 2))
        screen.blit(prompt_text, (SCREEN_WIDTH / 2 - prompt_text.get_width() / 2,
                                  SCREEN_HEIGHT / 2))
        screen.blit(user_input_text, (SCREEN_WIDTH / 2 - user_input_text.get_width() / 2,
                                      SCREEN_HEIGHT / 2 + FONT_SIZE))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_RETURN:
                    if user_input.isdigit() and int(user_input) > 0:
                        return int(user_input) * 60
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

def main():
    global bip39_words
    # Load BIP39 words
    with open("english.txt") as file:
        bip39_words = file.read().splitlines()

    running = True

    while running:
        # Show welcome screen and get duration from user input
        duration_seconds = welcome_screen()

        word = Word()
        score = 0

        start_time = time.time()

        while time.time() - start_time < duration_seconds:
            elapsed_time = int(time.time() - start_time)
            remaining_time = duration_seconds - elapsed_time

            # Fill the screen with black
            screen.fill(BLACK)

            # Render the current word and update its state
            word.render()

            # Display score and timer
            display_score_and_timer(score, remaining_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        exit()
                    elif event.unicode and not word.index >= len(word.word):
                        if event.unicode == word.word[word.index]:
                            word.index += 1
                            if word.index == len(word.word):  # Word completed
                                score += 1
                                word = Word()  # Get a new word

            pygame.display.flip()
            clock.tick(60)

        # Game over screen
        screen.fill(BLACK)
        game_over_surface = letterFont.render(f'Game Over! Your score: {score}', True, WHITE)
        play_again_surface = letterFont.render('Do you want to play again? (y/n)', True, WHITE)

        screen.blit(game_over_surface, (SCREEN_WIDTH / 2 - game_over_surface.get_width() / 2,
                                         SCREEN_HEIGHT / 2 - game_over_surface.get_height() / 2))
        screen.blit(play_again_surface, (SCREEN_WIDTH / 2 - play_again_surface.get_width() / 2,
                                          SCREEN_HEIGHT / 2 + FONT_SIZE))

        pygame.display.flip()

        waiting_for_input = True

        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        waiting_for_input = False
                        pygame.quit()
                        exit()
                    elif event.unicode.lower() == 'y':
                        waiting_for_input = False
                    elif event.unicode.lower() == 'n':
                        running = False
                        waiting_for_input = False

if __name__ == "__main__":
    main()
