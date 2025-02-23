### FALLING LETTERS GAME ###

# Anything with a # infront of it is a comment
# This means that it is a helpful note for whoever is reading the code
# and will not be executed as computer code

# Import pygame and other module
import pygame
import random
import time
import sys

from pygame.locals import *

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# How fast is the letter falling
speed = 5

# Lists of characters
allcaps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
lowercase = []
for x in allcaps:
    lowercase.append(x.lower())
specials = [',', '.', ';', ':', "'", '[', ']', '{', '}', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')' ]

# Harder lists for increased difficulty
medium = allcaps + lowercase
hard = medium + specials

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
t = 0

# System Font
letterFont = pygame.font.SysFont('Rockwell', 40)
textFont = pygame.font.SysFont('Rockwell', 20)

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Letter(pygame.sprite.Sprite):
    def __init__(self):
        super(Letter, self).__init__()
        self.char = lowercase[random.randint(0, len(lowercase)-1)]
        self.surf = letterFont.render(self.char, True, (255, 0, 0))
        self.rect = self.surf.get_rect(
            center = (random.randint(20, SCREEN_WIDTH - 20),0))

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create score counter
score = 0
scoretext = textFont.render("Score: "+str(score), True, (0, 200, 0), (0,0,0))

# Create average time counter
avgtime = 0
timetext = textFont.render("Average Time: "+str(avgtime), True, (255, 255, 0), (0,0,0))

# Create our messages that will display at the end
endgame = letterFont.render('Game Over!', True, (200, 0, 0))
playagain = textFont.render('Play again? [y/n]', True, (0, 0, 200))

# Instantiate a letter
letter = Letter()

# Create some boolean switches
running = True
gameover = False

# Main loop - everything in this loop happens over and over again
while running:

    # 60 frames per second
    clock.tick(60)

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Display the score and avgtime counters
    screen.blit(scoretext, (20, 20))
    screen.blit(timetext, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50))

    # Display the falling letter on the screen
    screen.blit(letter.surf, letter.rect)

    # Move letter down by the amount of speed (every single iteration)
    letter.rect.move_ip(0, speed)

    # Look at every event in the queue
    for event in pygame.event.get():

        if event.type == TEXTINPUT:

            if event.text == letter.char and not gameover:
                letter.kill()
                letter = Letter()
                score += 1
                avgtime = round((avgtime + t/100) / 2, 2)
                scoretext = textFont.render("Score: "+str(score), True, (0, 200, 0), (0,0,0))
                timetext = textFont.render("Average Time: "+str(avgtime), True, (255, 255, 0), (0,0,0))
                t = 0

        if event.type == TEXTINPUT and gameover:
            if event.text == 'y':
                letter.kill()
                letter = Letter()
                score = 0
                scoretext = textFont.render("Score: "+str(score), True, (0, 200, 0), (0,0,0))
                timetext = textFont.render("Average Time: "+str(0), True, (255, 255, 0), (0,0,0))
                t = 0
                gameover = False

            if event.text == 'n' and gameover:
                gameover = True
                running = False

        # Did user press the Escape key? If so, stop the loop.
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    # Did the falling letter reach the bottom of screen?
    if letter.rect.bottom >= SCREEN_HEIGHT:
        letter.rect.bottom = SCREEN_HEIGHT
        screen.blit(endgame, (SCREEN_WIDTH/2 - 100,SCREEN_HEIGHT/2 - 100))
        gameover = True
        screen.blit(playagain, (SCREEN_WIDTH/2 - 40,SCREEN_HEIGHT/2 - 20))

    # Update the display
    pygame.display.flip()
    t += 1
