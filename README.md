# Snake Game

A classic Snake Game built using Python and Pygame. Enjoy the retro gaming experience!

## Features

- Start screen with instructions
- Arrow-key snake movement
- Food spawning
- Score tracking
- Collision detection
- Wall collision
- Self collision
- Game over screen with replay support
- Pause and resume with P
- Difficulty selection (Easy, Medium, Hard)
- Persistent high score tracking
- Darker green snake body color for better visibility

## Technologies Used

- Python 3
- Pygame

## How to Run

Install pygame:

```bash
py -m pip install -r requirements.txt
```

Run the game:

```bash
py main.py
```

## Project Structure

- `main.py` – game entry point and loop
- `snake.py` – snake movement and collision logic
- `food.py` – food spawning and position management
- `settings.py` – shared game configuration constants
- `scripts/generate_commits.py` – optional local commit generator for GitHub contribution testing

## Generating Many Commits

If you want to create many local commits to populate a GitHub contribution graph, use `generate_commits.py`.

1. Confirm your Git identity matches your GitHub account:

```powershell
git config user.name "Your Name"
git config user.email "you@example.com"
```

2. Generate commits in the current repo:

```powershell
python generate_commits.py --count 200 --days 60
```

3. Push them to your remote repository branch:

```powershell
git push origin HEAD
```

4. Verify the author email matches a verified email on GitHub and wait a few minutes for GitHub to update your contribution graph.

> If commits still do not appear, check `git log --oneline --format="%h %an <%ae> %ad" -n 5` to confirm the author email and date.

## Future Improvements

- Sound effects
- Better graphics
- Obstacles and power-ups
- Additional game modes
- Leaderboard support
- Daily challenge mode
- Score-based speed boosts
- Bonus food ideas

## Learning Goals

This project is being developed to learn:

- Python programming
- Object-Oriented Programming
- Game development with Pygame
- Git and GitHub
- Software project structure

## Author

Shivang Dutta
