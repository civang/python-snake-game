import math
import sys
from array import array

import pygame

from food import Food
from game_utils import get_difficulty_fps, load_high_score, save_high_score
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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

title_font = pygame.font.SysFont(None, 64)
menu_font = pygame.font.SysFont(None, 36)
score_font = pygame.font.SysFont(None, 28)


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
        draw_text("Snake Game", title_font, GREEN, (WIDTH // 2, HEIGHT // 2 - 120))
        draw_text("Press ENTER to start", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 - 40))
        draw_text("Use arrow keys to move", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2))
        draw_text("Difficulty: 1 Easy  2 Medium  3 Hard", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 + 40))
        draw_text(f"Current: {difficulty.title()}", menu_font, GREEN, (WIDTH // 2, HEIGHT // 2 + 80))
        draw_text("Press ESC to quit", menu_font, WHITE, (WIDTH // 2, HEIGHT // 2 + 120))
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
    bar_x = WIDTH - 120
    bar_y = 18
    bar_width = 90
    bar_height = 18

    draw_text("Music", score_font, WHITE, (bar_x + 45, bar_y - 10))

    for index in range(6):
        wave = abs(math.sin(frame_offset + index * 0.7))
        height = int(6 + wave * 12)
        rect_height = max(4, height)
        rect_y = bar_y + (bar_height - rect_height) // 2
        rect_x = bar_x + index * 14
        pygame.draw.rect(screen, GREEN, (rect_x, rect_y, 10, rect_height))


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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
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
        high_score_text = score_font.render(f"High Score: {high_score}", True, GREEN)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))

        if paused:
            draw_text("Paused", title_font, WHITE, (WIDTH // 2, HEIGHT // 2))

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
