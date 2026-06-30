#!/usr/bin/env python3
"""generate_commits.py

Create many local git commits (optionally push) with configurable dates.

WARNING: This script modifies your local git history by creating commits.
Use responsibly. The script does not store or transmit credentials.
"""
from __future__ import annotations

import argparse
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


def run(cmd, cwd=None, env=None):
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def git_config_value(repo: Path, key: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "config", "--get", key],
            cwd=str(repo),
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip() or None
    except subprocess.CalledProcessError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate many git commits with backdated timestamps")
    parser.add_argument("--count", "-n", type=int, default=100, help="Number of commits to create")
    parser.add_argument("--days", "-d", type=int, default=30, help="Number of days span to distribute commits over")
    parser.add_argument("--start-date", "-s", type=str, default=None, help="Start date (YYYY-MM-DD). Defaults to today minus days")
    parser.add_argument("--message", "-m", type=str, default="chore: small update", help="Commit message prefix")
    parser.add_argument("--repo", "-r", type=str, default='.', help="Path to git repo (default: current directory)")
    parser.add_argument("--author-name", type=str, default=None, help="Author name for commits")
    parser.add_argument("--author-email", type=str, default=None, help="Author email for commits")
    parser.add_argument("--branch", type=str, default=None, help="Create a new branch for generated commits")
    parser.add_argument("--push", action="store_true", help="Push to remote after creating commits")

    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / '.git').exists():
        raise SystemExit(f"Not a git repo: {repo}")

    if args.author_name is None:
        args.author_name = git_config_value(repo, "user.name")
    if args.author_email is None:
        args.author_email = git_config_value(repo, "user.email")

    if args.start_date:
        start = datetime.strptime(args.start_date, "%Y-%m-%d")
    else:
        start = datetime.now() - timedelta(days=args.days)

    if args.author_name:
        print(f"Using commit author name: {args.author_name}")
    if args.author_email:
        print(f"Using commit author email: {args.author_email}")
    if not args.author_name or not args.author_email:
        print("WARNING: No author name/email configured. Git will use the default identity, which may not match your GitHub account.")

    # Create an empty file to touch so commits have a tiny change if desired
    touch_path = repo / '.commit_marker'
    touch_path.write_text('commit marker')

    for i in range(args.count):
        # Distribute commits across the days span (wrap if count > days)
        day_index = (i * args.days) // max(1, args.count)
        commit_date = start + timedelta(days=day_index)
        # vary time to avoid exact duplicates
        commit_time = commit_date + timedelta(seconds=(i % 86400))
        iso_date = commit_time.strftime('%Y-%m-%dT%H:%M:%S')

        # modify marker file to produce a small change
        touch_path.write_text(f'commit {i} at {iso_date}')

        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = iso_date
        env['GIT_COMMITTER_DATE'] = iso_date
        if args.author_name:
            env['GIT_AUTHOR_NAME'] = args.author_name
            env['GIT_COMMITTER_NAME'] = args.author_name
        if args.author_email:
            env['GIT_AUTHOR_EMAIL'] = args.author_email
            env['GIT_COMMITTER_EMAIL'] = args.author_email

        # stage the marker change
        run(["git", "add", str(touch_path)], cwd=str(repo))

        # commit
        msg = f"{args.message} #{i+1}"
        run(["git", "commit", "-m", msg], cwd=str(repo), env=env)

    print(f"Created {args.count} commits in {repo}")

    if args.push:
        push_target = ["git", "push"]
        if args.branch:
            push_target = ["git", "push", "-u", "origin", args.branch]
        print("Pushing to origin...")
        run(push_target, cwd=str(repo))


if __name__ == '__main__':
    main()
