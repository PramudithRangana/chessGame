# Chess Game Project

This is a simple implementation of a chess game using the Pygame library.

## Project Overview

The Chess Game project implements a basic chess game interface where players can make moves, including handling pawn promotions and demotions. The project is written in Python and uses the Pygame library for the graphical user interface.

### Features

- Chessboard visualization with pieces represented by images.
- Player can select and move pieces by clicking on squares.
- Supports standard chess rules, including en passant and castling.
- Handles pawn promotions and demotions.
- Implements undo and redo functionality for moves.
- Displays game over messages for checkmate, stalemate, and draw conditions.
- Allows players to restart the game or exit after a game over.

## Setup

1. Install the required libraries:

   ```
   pip install pygame chess
   ```

2. Download chess piece images and place them in the appropriate directory:
   - `src_images/small sizes/King-Gold.png`
   - `src_images/small sizes/King-Silver.png`
   - ... (other piece images)

3. Run the `chess_game.py` script to start the game:

   ```
   python chess_game.py
   ```

## Usage

- Click on a piece to select it.
- Click on a valid target square to move the selected piece.
- For pawn promotion, select the piece to promote to.
- Use Ctrl + Z for undo and Ctrl + Y for redo.

## File Structure

```
project_folder/
|-- chess_game.py
|-- src_images/
|   |-- small sizes/
|       |-- King-Gold.png
|       |-- King-Silver.png
|       |-- ... (other piece images)
```

## Dependencies

- Pygame
- Chess

## Acknowledgments

The project utilizes the Pygame library for graphical interface and the chess library for chess-related operations.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
