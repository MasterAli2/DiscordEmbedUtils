# Discord Embed utils

A silly flask server/website that allows you to use/play stuff in any discord server you have embed perms in.

This was mostly inspired by [Doom In Discord](https://doom.p2r3.com/)

## Features

- Play chess, tiktaktoe, connect 4 or minesweeper within discord

## Requirements

- Python 3.10+
- Linux (tested on Ubuntu)
- Also everything in `requirements.txt`
- Also some stuff like stockfish require apt packages

## Setup

1. Clone this repository
2. Run `./scripts/setup.sh`
3. Configure `config.py`
4. Run either with `./scripts/run_debug.sh` or with a WSGI server

Note: Make sure the domain does not contain the appending suffix (default is 'z')

## How To

## Games:
### Chess:
1. Send `https://[domain]/games/chess/z` in discord
2. Play by typing `s/z/[move]z` (ex: `s/z/e4z`) (algebraic notation)

### Tik Tak Toe:
1. Send `https://[domain]/games/ttt/z` in discord
2. Play by typing `s/z/[move]z` (ex: `s/z/5z`) (number)

### Connect 4:
1. Send `https://[domain]/games/four/z` in discord
2. Play by typing `s/z/[move]z` (ex: `s/z/2z`) (number)

### Mine Sweeper:
1. Send `https://[domain]/games/ms/z` in discord
2. Play by typing `s/z/[move]z` (ex: `s/z/2z`) (number)

