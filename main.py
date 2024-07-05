import pygame
import cv2
from hand_tracking import HandTracker
from games.flappy_bird import flappy_bird
from games.brick_breaker import brick_breaker
from games.pong import pong
from games.space_invaders import space_invaders

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Controlled Arcade")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# OpenCV setup - change the index here to select the desired camera
camera_index = 1  # Change this to the index of the desired camera
cap = cv2.VideoCapture(camera_index)
hand_tracker = HandTracker()

# Game states
MENU = 0
FLAPPY_BIRD = 1
BRICK_BREAKER = 2
PONG = 3
SPACE_INVADERS = 4
EXIT = 5
PAUSE = 6

# Main game loop
running = True
state = MENU
current_game = None
clock = pygame.time.Clock()

def draw_menu(cursor_position):
    win.fill(BLACK)
    font = pygame.font.Font(None, 48)
    title = font.render("Hand Controlled Arcade", True, WHITE)
    win.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    font = pygame.font.Font(None, 36)
    options = ["Flappy Bird", "Brick Breaker", "Pong", "Space Invaders", "Exit"]
    for i, option in enumerate(options):
        text = font.render(option, True, WHITE)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + i * 50))
    
    if cursor_position:
        pygame.draw.circle(win, GREEN, cursor_position, 10)
    
    pygame.display.flip()

def draw_pause():
    win.fill(BLACK)
    font = pygame.font.Font(None, 36)
    options = ["Resume", "Exit to Main Menu"]
    for i, option in enumerate(options):
        text = font.render(option, True, WHITE)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 50))
    pygame.display.flip()

while running:
    ret, frame = cap.read()
    if not ret:
        break
    hand_positions, frame = hand_tracker.get_hand_position(frame)
    gesture = hand_tracker.is_gesture(hand_positions)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    cursor_position = None
    if hand_positions:
        cursor_position = (hand_positions[0][8][0], hand_positions[0][8][1])
    
    if state == MENU:
        draw_menu(cursor_position)
        if gesture and cursor_position:
            _, y = cursor_position
            if 150 < y < 200:
                state = FLAPPY_BIRD
                current_game = FLAPPY_BIRD
            elif 200 < y < 250:
                state = BRICK_BREAKER
                current_game = BRICK_BREAKER
            elif 250 < y < 300:
                state = PONG
                current_game = PONG
            elif 300 < y < 350:
                state = SPACE_INVADERS
                current_game = SPACE_INVADERS
            elif 350 < y < 400:
                state = EXIT

    elif state == PAUSE:
        draw_pause()
        if gesture:
            if hand_positions:
                _, y = hand_positions[0][8]
                if 200 < y < 250:
                    state = current_game  # Resume current game
                elif 250 < y < 300:
                    state = MENU

    elif state == FLAPPY_BIRD:
        flappy_bird(win, hand_tracker, cap)
        state = MENU

    elif state == BRICK_BREAKER:
        brick_breaker(win, hand_tracker, cap)
        state = MENU

    elif state == PONG:
        pong(win, hand_tracker, cap)
        state = MENU

    elif state == SPACE_INVADERS:
        space_invaders(win, hand_tracker, cap)
        state = MENU

    elif state == EXIT:
        running = False

    # Show frame with hand tracking
    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()