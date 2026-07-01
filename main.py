import math
import sys
from array import array

import pygame

from food import Food
from game_utils import get_difficulty_fps, get_pause_message, load_high_score, save_high_score
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

try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
    audio_enabled = True
except pygame.error:
    audio_enabled = False

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# initialize fonts to None; they will be created in recompute_layout
title_font = None
menu_font = None
score_font = None

# Current window size and rendering layout (updated on resize)
win_width, win_height = WIDTH, HEIGHT
cell_render_size = CELL_SIZE
offset_x = 0
offset_y = 0


def recompute_layout(w, h):
    global win_width, win_height, cell_render_size, offset_x, offset_y
    global title_font, menu_font, score_font
    win_width, win_height = w, h
    # Determine the largest integer cell size that fits the logical grid
    cell_render_size = max(4, min(win_width // COLS, win_height // ROWS))
    grid_w = cell_render_size * COLS
    grid_h = cell_render_size * ROWS
    offset_x = (win_width - grid_w) // 2
    offset_y = (win_height - grid_h) // 2

    # Recreate fonts scaled to window width for readability
    title_size = max(24, win_width // 12)
    menu_size = max(14, win_width // 34)
    score_size = max(12, win_width // 48)
    title_font = pygame.font.SysFont(None, title_size)
    menu_font = pygame.font.SysFont(None, menu_size)
    score_font = pygame.font.SysFont(None, score_size)


# initialize layout and fonts
recompute_layout(win_width, win_height)


def build_tone(frequency, duration=0.12, volume=0.06):
    if not audio_enabled:
        return None

    sample_rate = 22050
    amplitude = int(32767 * volume)
    sample_count = int(duration * sample_rate)
    data = array("h")

    for index in range(sample_count):
        value = int(amplitude * math.sin(2 * math.pi * frequency * index / sample_rate))
        data.append(value)

    return pygame.mixer.Sound(buffer=data.tobytes())


music_notes = [261.63, 329.63, 392.00, 493.88, 392.00, 329.63]
music_sounds = [build_tone(note) for note in music_notes]


def draw_text(text, font, color, center):
    label = font.render(text, True, color)
    rect = label.get_rect(center=center)
    screen.blit(label, rect)


def draw_panel(x, y, width, height, color, border_color, radius=18):
    pygame.draw.rect(screen, (0, 0, 0), (x + 4, y + 4, width, height), border_radius=radius)
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=radius)
    pygame.draw.rect(screen, border_color, (x, y, width, height), width=3, border_radius=radius)


def show_start_screen():
    difficulty = "medium"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return difficulty
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_1:
                    difficulty = "easy"
                if event.key == pygame.K_2:
                    difficulty = "medium"
                if event.key == pygame.K_3:
                    difficulty = "hard"

        screen.fill(BLACK)

        for x in range(0, win_width, 40):
            pygame.draw.line(screen, (18, 28, 18), (x, 0), (x, win_height), 1)
        for y in range(0, win_height, 40):
            pygame.draw.line(screen, (18, 28, 18), (0, y), (win_width, y), 1)

        panel_width = min(560, max(340, win_width - 80))
        panel_height = min(420, max(320, win_height - 80))
        panel_x = (win_width - panel_width) // 2
        panel_y = (win_height - panel_height) // 2
        draw_panel(panel_x, panel_y, panel_width, panel_height, (18, 24, 18), GREEN, 24)

        draw_text("SNAKE", title_font, (0, 0, 0), (win_width // 2 + 3, panel_y + 70 + 3))
        draw_text("SNAKE", title_font, GREEN, (win_width // 2, panel_y + 70))
        draw_text("Classic Arcade", menu_font, WHITE, (win_width // 2, panel_y + 120))
        draw_text("Press ENTER to start", menu_font, (255, 255, 255), (win_width // 2, panel_y + 170))
        draw_text("Use arrow keys to move", menu_font, (220, 220, 220), (win_width // 2, panel_y + 210))
        draw_text("Difficulty: 1 Easy   2 Medium   3 Hard", menu_font, (230, 230, 230), (win_width // 2, panel_y + 250))
        draw_text(f"Current: {difficulty.title()}", menu_font, GREEN, (win_width // 2, panel_y + 290))
        draw_text("P = pause  •  ESC = quit", menu_font, (200, 200, 200), (win_width // 2, panel_y + 330))
        draw_text("Eat food to grow faster and score more", menu_font, (180, 220, 180), (win_width // 2, panel_y + 366))

        pygame.display.flip()
        clock.tick(15)


def show_game_over_screen(score, high_score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "play_again"
                if event.key == pygame.K_m:
                    return "main_menu"
                if event.key == pygame.K_ESCAPE:
                    return "quit"

        screen.fill(BLACK)
        draw_text("Game Over", title_font, RED, (WIDTH // 2, HEIGHT // 2 - 120))
        draw_text(f"Final Score: {score}", title_font, WHITE, (WIDTH // 2, HEIGHT // 2 - 40))
        draw_text(f"High Score: {high_score}", title_font, GREEN, (WIDTH // 2, HEIGHT // 2 + 20))
        draw_text("Press ENTER to play again", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 + 80))
        draw_text("Press M for Main Menu", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 + 120))
        draw_text("Press ESC to quit", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 + 160))
        pygame.display.flip()
        clock.tick(15)


def draw_music_bar(frame_offset):
    bar_x = win_width - 140
    bar_y = 18
    bar_width = 110
    bar_height = 18

    draw_text("Music", score_font, WHITE, (bar_x + bar_width // 2, bar_y - 10))

    for index in range(6):
        wave = abs(math.sin(frame_offset + index * 0.7))
        height = int(6 + wave * 12)
        rect_height = max(4, height)
        rect_y = bar_y + (bar_height - rect_height) // 2
        rect_x = bar_x + index * 16
        pygame.draw.rect(screen, GREEN, (rect_x, rect_y, 12, rect_height))


def run_game(difficulty):
    snake = Snake()
    food = Food(snake.body)
    score = 0
    running = True
    paused = False
    music_counter = 0
    fps = get_difficulty_fps(difficulty)
    high_score = load_high_score()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                # rebuild screen surface and layout for new size
                global screen
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                recompute_layout(event.w, event.h)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_c and paused:
                    paused = False
                elif event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        if not paused:
            ate_food = snake.head() == food.position
            snake.move(grow=ate_food)

            if ate_food:
                score += 1
                if score > high_score:
                    high_score = score
                food = Food(snake.body)

            if snake.is_out_of_bounds() or snake.collides_with_self():
                running = False

        screen.fill(BLACK)

        # Draw food and snake using scaled cell size and centered grid
        fx, fy = food.position
        pygame.draw.rect(
            screen,
            RED,
            (
                offset_x + fx * cell_render_size,
                offset_y + fy * cell_render_size,
                cell_render_size,
                cell_render_size,
            ),
        )

        for segment in snake.body:
            x, y = segment
            pygame.draw.rect(
                screen,
                GREEN,
                (
                    offset_x + x * cell_render_size,
                    offset_y + y * cell_render_size,
                    cell_render_size,
                    cell_render_size,
                ),
            )

        score_text = score_font.render(f"Score: {score}", True, WHITE)
        high_score_text = score_font.render(f"High Score: {high_score}", True, GREEN)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))

        if paused:
            draw_text("Paused", title_font, WHITE, (win_width // 2, win_height // 2 - 20))
            draw_text(get_pause_message(paused), menu_font, GREEN, (win_width // 2, win_height // 2 + 20))

        frame_offset = pygame.time.get_ticks() / 240.0
        draw_music_bar(frame_offset)

        if audio_enabled and music_counter % 12 == 0:
            note_sound = music_sounds[music_counter // 12 % len(music_sounds)]
            if note_sound is not None:
                note_sound.play()

        music_counter += 1
        pygame.display.update()
        clock.tick(fps)

    save_high_score(score)
    return score, high_score


def main():
    while True:
        difficulty = show_start_screen()

        while True:
            final_score, high_score = run_game(difficulty)
            choice = show_game_over_screen(final_score, high_score)

            if choice == "play_again":
                continue
            if choice == "main_menu":
                break
            if choice == "quit":
                pygame.quit()
                sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
