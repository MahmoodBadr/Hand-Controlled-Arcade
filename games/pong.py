import pygame
import cv2

def pong(win, hand_tracker, cap):
    WIDTH, HEIGHT = win.get_size()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    paddle_width = 20
    paddle_height = 100
    paddle_speed = 10

    ball_radius = 10
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = 5
    ball_dy = 5

    player_y = HEIGHT // 2 - paddle_height // 2
    ai_y = HEIGHT // 2 - paddle_height // 2
    ai_speed = 5

    player_score = 0
    ai_score = 0
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    running = True

    while running:
        ret, frame = cap.read()
        if not ret:
            break
        hand_positions, frame = hand_tracker.get_hand_position(frame)
        gesture = hand_tracker.is_gesture(hand_positions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        if hand_positions:
            _, y = hand_positions[0][8]
            player_y = y - paddle_height // 2

        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y - ball_radius < 0 or ball_y + ball_radius > HEIGHT:
            ball_dy *= -1

        if ball_x - ball_radius < paddle_width and player_y < ball_y < player_y + paddle_height:
            ball_dx *= -1

        if ball_x + ball_radius > WIDTH - paddle_width and ai_y < ball_y < ai_y + paddle_height:
            ball_dx *= -1

        if ball_x - ball_radius < 0:
            ai_score += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_dx *= -1

        if ball_x + ball_radius > WIDTH:
            player_score += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_dx *= -1

        ai_y += (ball_y - (ai_y + paddle_height // 2)) * ai_speed / WIDTH

        win.fill(BLACK)
        pygame.draw.rect(win, WHITE, (0, player_y, paddle_width, paddle_height))
        pygame.draw.rect(win, WHITE, (WIDTH - paddle_width, ai_y, paddle_width, paddle_height))
        pygame.draw.circle(win, WHITE, (ball_x, ball_y), ball_radius)

        player_score_text = font.render(f"Player: {player_score}", True, WHITE)
        win.blit(player_score_text, (10, 10))
        ai_score_text = font.render(f"AI: {ai_score}", True, WHITE)
        win.blit(ai_score_text, (WIDTH - ai_score_text.get_width() - 10, 10))
        pygame.display.flip()
        clock.tick(60)

        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
