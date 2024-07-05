import pygame
import cv2

def flappy_bird(win, hand_tracker, cap):
    # Initialize game variables
    WIDTH, HEIGHT = win.get_size()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    bird_y = HEIGHT // 2
    bird_x = WIDTH // 4
    bird_radius = 20
    bird_velocity = 0
    gravity = 0.5
    flap_power = -10
    pipe_width = 80
    pipe_gap = 200
    pipe_speed = 5
    pipes = [(WIDTH, HEIGHT // 2 - pipe_gap // 2)]
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

        # Hand control
        if hand_positions:
            _, y = hand_positions[0][8]
            if y < HEIGHT // 2:
                bird_velocity = flap_power

        # Update bird
        bird_velocity += gravity
        bird_y += bird_velocity

        # Update pipes
        new_pipes = []
        for pipe_x, pipe_y in pipes:
            pipe_x -= pipe_speed
            if pipe_x + pipe_width > 0:
                new_pipes.append((pipe_x, pipe_y))
            else:
                score += 1
        pipes = new_pipes

        if len(pipes) < 5 and pipes[-1][0] < WIDTH - 300:
            pipes.append((WIDTH, HEIGHT // 2 - pipe_gap // 2))

        # Collision detection
        if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
            running = False
            return
        for pipe_x, pipe_y in pipes:
            if pipe_x < bird_x < pipe_x + pipe_width:
                if bird_y - bird_radius < pipe_y or bird_y + bird_radius > pipe_y + pipe_gap:
                    running = False
                    return

        # Draw everything
        win.fill(BLACK)
        pygame.draw.circle(win, RED, (bird_x, bird_y), bird_radius)
        for pipe_x, pipe_y in pipes:
            pygame.draw.rect(win, WHITE, (pipe_x, 0, pipe_width, pipe_y))
            pygame.draw.rect(win, WHITE, (pipe_x, pipe_y + pipe_gap, pipe_width, HEIGHT - pipe_y - pipe_gap))
        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

        # Show frame with hand tracking
        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
