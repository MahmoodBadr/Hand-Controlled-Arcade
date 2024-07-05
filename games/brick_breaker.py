import pygame
import cv2

def brick_breaker(win, hand_tracker, cap):
    WIDTH, HEIGHT = win.get_size()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    paddle_width = 100
    paddle_height = 20
    paddle_y = HEIGHT - 30
    paddle_x = WIDTH // 2 - paddle_width // 2

    ball_radius = 10
    ball_x = WIDTH // 2
    ball_y = paddle_y - ball_radius
    ball_dx = 5
    ball_dy = -5

    brick_rows = 5
    brick_cols = 10
    brick_width = WIDTH // brick_cols
    brick_height = 20
    bricks = [[True] * brick_cols for _ in range(brick_rows)]

    score = 0
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
            x, _ = hand_positions[0][8]
            paddle_x = x - paddle_width // 2

        ball_x += ball_dx
        ball_y += ball_dy

        if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
            ball_dx *= -1
        if ball_y - ball_radius < 0:
            ball_dy *= -1

        if paddle_x < ball_x < paddle_x + paddle_width and paddle_y < ball_y + ball_radius < paddle_y + paddle_height:
            ball_dy *= -1

        for i in range(brick_rows):
            for j in range(brick_cols):
                if bricks[i][j]:
                    brick_x = j * brick_width
                    brick_y = i * brick_height
                    if brick_x < ball_x < brick_x + brick_width and brick_y < ball_y < brick_y + brick_height:
                        ball_dy *= -1
                        bricks[i][j] = False
                        score += 1

        if ball_y - ball_radius > HEIGHT:
            running = False
            return

        win.fill(BLACK)
        pygame.draw.rect(win, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))
        pygame.draw.circle(win, RED, (ball_x, ball_y), ball_radius)

        for i in range(brick_rows):
            for j in range(brick_cols):
                if bricks[i][j]:
                    brick_x = j * brick_width
                    brick_y = i * brick_height
                    pygame.draw.rect(win, WHITE, (brick_x, brick_y, brick_width, brick_height))

        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
