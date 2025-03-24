### FALLING WORDS TYPING GAME (FINAL VERSION) ###

import pygame
import random
import time
import sys

from pygame.locals import *

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BASE_SPEED = 2  # Velocidad inicial
SPEED_INCREMENT = 0.05  # Incremento por cada 10 puntos
WORD_FILE = 'english.txt'

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load words from file
try:
    with open(WORD_FILE, 'r') as f:
        word_list = [line.strip().lower() for line in f]
except FileNotFoundError:
    print(f"Error: {WORD_FILE} not found!")
    sys.exit()

# Fonts
word_font = pygame.font.SysFont('Rockwell', 40)
ui_font = pygame.font.SysFont('Rockwell', 20)

class FallingWord(pygame.sprite.Sprite):
    def __init__(self, word, speed):
        super().__init__()
        self.word = word
        self.typed_length = 0
        self.speed = speed
        self.update_surface()
        self.rect = self.surf.get_rect(
            center=(random.randint(100, SCREEN_WIDTH-100), 0)
        )

    def update_surface(self):
        # Create surface with individual character coloring
        characters = []
        total_width = 0
        max_height = 0

        # Create surfaces for each character
        for i, char in enumerate(self.word):
            color = (0, 0, 255) if i < self.typed_length else (255, 0, 0)
            char_surf = word_font.render(char, True, color)
            characters.append((char_surf, total_width))
            total_width += char_surf.get_width()
            max_height = max(max_height, char_surf.get_height())

        # Create final surface
        self.surf = pygame.Surface((total_width, max_height), pygame.SRCALPHA)
        for char_surf, x_pos in characters:
            self.surf.blit(char_surf, (x_pos, 0))

# Game state
current_word = None
input_buffer = []
score = 0
avg_time = 0
start_time = 0
running = True
game_over = False

def calculate_speed():
    return BASE_SPEED + (score // 10) * SPEED_INCREMENT

def spawn_new_word():
    global current_word, start_time
    current_word = FallingWord(random.choice(word_list), calculate_speed())
    start_time = time.time()

def reset_game():
    global score, avg_time, input_buffer
    score = 0
    avg_time = 0
    input_buffer = []
    spawn_new_word()

spawn_new_word()

# Main game loop
while running:
    clock.tick(60)
    screen.fill((255, 255, 255))

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if game_over:
                if event.key == K_y:
                    reset_game()
                    game_over = False
                elif event.key == K_n:
                    running = False
            else:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_BACKSPACE:
                    if input_buffer:
                        input_buffer.pop()
                elif event.unicode.isalpha():
                    input_buffer.append(event.unicode.lower())

    if not game_over:
        # Check input against current word
        if current_word:
            current_attempt = ''.join(input_buffer)

            # Update typed progress
            current_word.typed_length = 0
            for i, (input_char, word_char) in enumerate(zip(input_buffer, current_word.word)):
                if input_char == word_char:
                    current_word.typed_length += 1
                else:
                    break
            current_word.update_surface()

            if current_attempt == current_word.word:
                # Correct word typed
                time_taken = time.time() - start_time
                avg_time = (avg_time + time_taken) / 2 if score > 0 else time_taken
                score += 1
                input_buffer = []
                spawn_new_word()
            elif not current_word.word.startswith(current_attempt):
                # Wrong character typed
                input_buffer = []

            # Move word down
            current_word.rect.move_ip(0, current_word.speed)
            screen.blit(current_word.surf, current_word.rect)

            # Check if word hit bottom
            if current_word.rect.bottom >= SCREEN_HEIGHT:
                game_over = True

    # Update UI elements
    score_surf = ui_font.render(f"Score: {score}", True, (0, 200, 0))
    time_surf = ui_font.render(f"Avg Time: {avg_time:.2f}s", True, (0, 0, 0))
    screen.blit(score_surf, (20, 20))
    screen.blit(time_surf, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50))

    # Game over screen
    if game_over:
        game_over_surf = word_font.render('GAME OVER', True, (255, 0, 0))
        replay_surf = ui_font.render('Play again? (Y/N)', True, (0, 0, 255))
        screen.blit(game_over_surf, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
        screen.blit(replay_surf, (SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 20))

    pygame.display.flip()

pygame.quit()
