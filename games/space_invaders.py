import pygame
import cv2

def space_invaders(win, hand_tracker, cap):
    WIDTH, HEIGHT = win.get_size()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    player_width = 50
    player_height = 20
    player_y = HEIGHT - 30
    player_x = WIDTH // 2 - player_width // 2

    bullet_width = 5
    bullet_height = 10
    bullet_speed = -10
    bullets = []

    alien_width = 40
    alien_height = 30
    alien_speed = 5
    aliens = [(x, y) for x in range(50, WIDTH - 50, 60) for y in range(50, 200, 50)]
    alien_direction = 1

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
            player_x = x - player_width // 2

        if gesture:
            bullets.append((player_x + player_width // 2, player_y))

        new_bullets = []
        for bullet_x, bullet_y in bullets:
            bullet_y += bullet_speed
            if bullet_y > 0:
                new_bullets.append((bullet_x, bullet_y))
        bullets = new_bullets

        for i, (alien_x, alien_y) in enumerate(aliens):
            if alien_x + alien_direction * alien_speed < 0 or alien_x + alien_direction * alien_speed + alien_width > WIDTH:
                alien_direction *= -1
                aliens = [(x, y + 30) for x, y in aliens]
                break
        aliens = [(x + alien_direction * alien_speed, y) for x, y in aliens]

        new_aliens = []
        for alien_x, alien_y in aliens:
            hit = False
            for bullet_x, bullet_y in bullets:
                if alien_x < bullet_x < alien_x + alien_width and alien_y < bullet_y < alien_y + alien_height:
                    score += 1
                    hit = True
                    break
            if not hit:
                new_aliens.append((alien_x, alien_y))
        aliens = new_aliens

        if any(alien_y + alien_height > HEIGHT for _, alien_y in aliens):
            running = False
            running = False
            return

        win.fill(BLACK)
        pygame.draw.rect(win, GREEN, (player_x, player_y, player_width, player_height))
        for bullet_x, bullet_y in bullets:
            pygame.draw.rect(win, RED, (bullet_x, bullet_y, bullet_width, bullet_height))
        for alien_x, alien_y in aliens:
            pygame.draw.rect(win, WHITE, (alien_x, alien_y, alien_width, alien_height))

        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
