import pygame
import sys

from food import Food
from settings import (
    BLACK,
    CELL_SIZE,
    COLS,
    FPS,
    GREEN,
    HEIGHT,
    RED,
    ROWS,
    WHITE,
    WIDTH,
)
from snake import Snake

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

title_font = pygame.font.SysFont(None, 64)
menu_font = pygame.font.SysFont(None, 36)
score_font = pygame.font.SysFont(None, 28)


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
    snake = Snake()
    food = Food(snake.body)
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        ate_food = snake.head() == food.position
        snake.move(grow=ate_food)

        if ate_food:
            score += 1
            food = Food(snake.body)

        if snake.is_out_of_bounds() or snake.collides_with_self():
            running = False

        screen.fill(BLACK)

        pygame.draw.rect(
            screen,
            RED,
            (food.position[0] * CELL_SIZE, food.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )

        for segment in snake.body:
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
