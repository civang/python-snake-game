import pygame
import random
import sys

# ==========================
# CONFIGURATION
# ==========================

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
FPS = 10

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

title_font = pygame.font.SysFont(None, 64)
menu_font = pygame.font.SysFont(None, 36)
score_font = pygame.font.SysFont(None, 28)

# ==========================
# HELPERS
# ==========================

def draw_text(text, font, color, center):
    label = font.render(text, True, color)
    rect = label.get_rect(center=center)
    screen.blit(label, rect)


def show_start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        draw_text("Snake Game", title_font, GREEN, (WIDTH // 2, HEIGHT // 2 - 80))
        draw_text("Press ENTER to start", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2))
        draw_text("Use arrow keys to move", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 + 40))
        draw_text("Press ESC to quit", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 + 80))
        pygame.display.flip()
        clock.tick(15)


def show_game_over_screen(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

        screen.fill(BLACK)
        draw_text("Game Over", title_font, RED, (WIDTH // 2, HEIGHT // 2 - 80))
        draw_text(f"Final Score: {score}", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2))
        draw_text("Press ENTER to play again", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 + 40))
        draw_text("Press ESC to exit", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 + 80))
        pygame.display.flip()
        clock.tick(15)


def run_game():
    snake = [(10, 10)]
    direction = (1, 0)
    food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    score = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        head_x, head_y = snake[0]
        dir_x, dir_y = direction
        new_head = (head_x + dir_x, head_y + dir_y)

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            while True:
                food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
                if food not in snake:
                    break
        else:
            snake.pop()

        if (
            new_head[0] < 0
            or new_head[0] >= COLS
            or new_head[1] < 0
            or new_head[1] >= ROWS
        ):
            running = False

        if new_head in snake[1:]:
            running = False

        screen.fill(BLACK)

        pygame.draw.rect(
            screen,
            RED,
            (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )

        for segment in snake:
            x, y = segment
            pygame.draw.rect(
                screen,
                GREEN,
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

        score_text = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    return score


def main():
    while True:
        show_start_screen()
        final_score = run_game()
        if not show_game_over_screen(final_score):
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
