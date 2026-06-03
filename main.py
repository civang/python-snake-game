import pygame
import random
import sys

# ==========================
# INITIALIZATION
# ==========================

pygame.init()

# Window Settings
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Create Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)

# ==========================
# GAME DATA
# ==========================

snake = [(10, 10)]
direction = (1, 0)

food = (
    random.randint(0, COLS - 1),
    random.randint(0, ROWS - 1)
)

score = 0

# ==========================
# GAME LOOP
# ==========================

running = True

while running:

    # ----------------------
    # EVENTS
    # ----------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)

            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)

            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)

            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # ----------------------
    # MOVE SNAKE
    # ----------------------

    head_x, head_y = snake[0]

    dir_x, dir_y = direction

    new_head = (
        head_x + dir_x,
        head_y + dir_y
    )

    snake.insert(0, new_head)

    # ----------------------
    # FOOD COLLISION
    # ----------------------

    if new_head == food:

        score += 1

        food = (
            random.randint(0, COLS - 1),
            random.randint(0, ROWS - 1)
        )

    else:
        snake.pop()

    # ----------------------
    # WALL COLLISION
    # ----------------------

    if (
        new_head[0] < 0
        or new_head[0] >= COLS
        or new_head[1] < 0
        or new_head[1] >= ROWS
    ):
        running = False

    # ----------------------
    # SELF COLLISION
    # ----------------------

    if new_head in snake[1:]:
        running = False

    # ----------------------
    # DRAW BACKGROUND
    # ----------------------

    screen.fill(BLACK)

    # ----------------------
    # DRAW FOOD
    # ----------------------

    pygame.draw.rect(
        screen,
        RED,
        (
            food[0] * CELL_SIZE,
            food[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )

    # ----------------------
    # DRAW SNAKE
    # ----------------------

    for segment in snake:

        x, y = segment

        pygame.draw.rect(
            screen,
            GREEN,
            (
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )

    # ----------------------
    # DRAW SCORE
    # ----------------------

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (10, 10))

    # ----------------------
    # UPDATE DISPLAY
    # ----------------------

    pygame.display.update()

    # ----------------------
    # FPS
    # ----------------------

    clock.tick(10)

# ==========================
# EXIT
# ==========================

pygame.quit()
sys.exit()