# ConnectN Game

ConnectN is a Python implementation of the classic game Connect Four with a twist—you can choose the number of consecutive discs required to win! The game includes an AI player, making it an engaging and challenging experience.

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/connectn.git
    cd connectn
    ```

2. Run the ConnectN game:

    ```bash
    python connectn 3 4 3
    ```

    This command sets up a ConnectN game with 3 rows, 4 columns, and a win streak of 3.

3. Follow the on-screen instructions to play the game. Enter the desired column number to drop a disc.

## Gameplay

ConnectN follows the rules of Connect Four but allows you to customize the number of consecutive discs required to win the game (N). This customization adds a new layer of strategy to the classic game.

- **Player vs. Player:** Two players take turns entering column numbers to drop their respective discs.

- **Player vs. AI:** Challenge yourself against an AI opponent with varying difficulty levels.

## Customization

Feel free to explore the code and customize the game further. You can adjust the board size, change the winning condition (N), or enhance the AI algorithm.

## Command-Line Options

The game supports the following command-line options:

- `-p` or `--players`: Set the number of players (1 or 2).
- `-n` or `--consecutive`: Set the number of consecutive discs required to win.
- `-d` or `--difficulty`: Set the AI difficulty level (easy, medium, hard).

Example:

```bash
python connectn -p 1 -n 5 -d hard
