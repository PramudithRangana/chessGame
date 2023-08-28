import traceback

import pygame
import chess


class ChessGame:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        pygame.font.init()  # Initialize Pygame's font module

        self.clock = pygame.time.Clock()

        # Calculate the dynamic board size based on the smaller screen dimension
        screen_info = pygame.display.Info()
        smaller_dimension = min(screen_info.current_w, screen_info.current_h - 100)
        self.board_size = smaller_dimension - 100  # You can adjust the padding as needed

        label_space = 30  # Space for smaller labels on each side

        # Create a larger surface to include space for labels
        self.screen = pygame.display.set_mode((self.board_size + label_space, self.board_size + label_space))
        pygame.display.set_caption("Chess Game")

        # Create a history list to store move details
        self.move_history = []

        # For undo, redo
        self.UNDO_EVENT = pygame.USEREVENT + 1
        self.REDO_EVENT = pygame.USEREVENT + 2

        # Define custom event types for undo and redo
        self.undo_event = pygame.event.Event(self.UNDO_EVENT)
        self.redo_event = pygame.event.Event(self.REDO_EVENT)

        self.undo_stack = []
        self.redo_stack = []

        self.redo_steps = []  # New list to store redo steps

        # Load chess piece images
        self.piece_images = {
            chess.Piece(chess.KING, chess.WHITE): pygame.image.load("src_images/small sizes/King-Gold.png"),
            chess.Piece(chess.KING, chess.BLACK): pygame.image.load("src_images/small sizes/King-Silver.png"),

            chess.Piece(chess.QUEEN, chess.WHITE): pygame.image.load("src_images/small sizes/Queen-Gold.png"),
            chess.Piece(chess.QUEEN, chess.BLACK): pygame.image.load("src_images/small sizes/Queen-Silver.png"),

            chess.Piece(chess.ROOK, chess.WHITE): pygame.image.load("src_images/small sizes/Rook-Gold.png"),
            chess.Piece(chess.ROOK, chess.BLACK): pygame.image.load("src_images/small sizes/Rook-Silver.png"),

            chess.Piece(chess.BISHOP, chess.WHITE): pygame.image.load("src_images/small sizes/Bishop-Gold.png"),
            chess.Piece(chess.BISHOP, chess.BLACK): pygame.image.load("src_images/small sizes/Bishop-Silver.png"),

            chess.Piece(chess.KNIGHT, chess.WHITE): pygame.image.load("src_images/small sizes/Knight-Gold.png"),
            chess.Piece(chess.KNIGHT, chess.BLACK): pygame.image.load("src_images/small sizes/Knight-Silver.png"),

            chess.Piece(chess.PAWN, chess.WHITE): pygame.image.load("src_images/small sizes/Pawn-Gold.png"),
            chess.Piece(chess.PAWN, chess.BLACK): pygame.image.load("src_images/small sizes/Pawn-Silver.png"),
        }

        # Initialize font for options
        self.font = pygame.font.Font(None, 36)

        self.WHITE = (239, 223, 197)
        self.BLACK = (90, 61, 41)

        self.current_player = None

        self.board = chess.Board()
        self.selected_piece = None
        self.target_square = None
        self.response = None

        self.selected_option = None
        self.valid_moves = []

    def calculate_valid_moves(self, selected_square):
        valid_moves = []
        if self.board.piece_at(selected_square):
            for move in self.board.legal_moves:
                if move.from_square == selected_square:
                    valid_moves.append(move.to_square)
                    if (
                            self.board.piece_at(selected_square).piece_type == chess.PAWN and
                            (chess.square_rank(move.to_square) == 0 or chess.square_rank(move.to_square) == 7)
                    ):
                        valid_moves.append(move.to_square + chess.QUEEN)
                        valid_moves.append(move.to_square + chess.ROOK)
                        valid_moves.append(move.to_square + chess.BISHOP)
                        valid_moves.append(move.to_square + chess.KNIGHT)
        return valid_moves

    def initialize_game(self):
        # Initialize or reset your game state here
        self.board = chess.Board()  # Initialize the game board as a chess.Board object
        self.current_player = "white"  # Set the starting player
        self.selected_piece = None  # Store the currently selected piece
        self.valid_moves = []  # Store valid moves for the selected piece
        # ... other game state variables ...

    def get_piece_at_square(self, row, col):
        square = chess.square(col, 7 - row)  # Convert to chess notation (row 0 is the bottom row in Pygame)
        piece = self.board.piece_at(square)
        return piece

    def initialize_board(self):
        # Create a 8x8 grid representing the chess board
        board = [[None] * 8 for _ in range(8)]

        # Initialize the board with piece images
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at_square(row, col)  # Implement this function to get the piece for the square
                if piece:
                    board[row][col] = self.piece_images[piece]

        return board

    def restart_game(self):
        # Reset any necessary game state or variables here
        # For example, reset the board, player positions, or any relevant game data
        self.initialize_game()
        self.initialize_board()

        # You might also need to reinitialize any UI elements or assets
        # For example, if you display a board, reinitialize it with starting positions

        # Clear the selected option from the previous game over screen
        self.selected_option = None

        # Resume the game loop
        self.run()

    def run(self):
        try:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_mouse_click(event)

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL:  # Ctrl + Z for Undo
                            self.undo()

                        elif event.key == pygame.K_y and event.mod & pygame.KMOD_CTRL:  # Ctrl + Y for Redo
                            self.redo()

                self.update_display()

                if self.board.is_game_over():
                    if self.board.is_checkmate():
                        winner = "white" if self.board.turn == chess.BLACK else "black"
                        options = ["Restart", "Exit"]  # You can add more options here if needed
                        self.response = self.display_message_with_options(f"{winner.capitalize()} player won!", options)

                    elif self.board.is_fivefold_repetition():
                        options = ["Restart", "Exit"]  # You can add more options here if needed
                        self.response = self.display_message_with_options(f"Match Drawn !", options)

                    elif self.board.is_stalemate():
                        options = ["Restart", "Exit"]  # You can add more options here if needed
                        self.response = self.display_message_with_options(f"Stalemate !", options)

                    if self.response == "Restart":
                        self.response = None
                        self.restart_game()
                    elif self.response == "Exit":
                        pygame.quit()
                        exit()

                pygame.display.flip()

            pygame.quit()

        except Exception as e:
            print("Error: ", e)
            print(traceback.format_exc())

    def display_message_with_options(self, message, options):
        font = pygame.font.Font(None, 48)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.board_size // 2, self.board_size // 2))

        button_rects = []
        button_texts = []

        for i, option in enumerate(options):
            button_rect = pygame.Rect((i + 1) * self.board_size // (len(options) + 1) - 100, self.board_size // 2 + 50,
                                      200, 50)
            button_rects.append(button_rect)

            button_text = font.render(option, True, (255, 255, 255))
            button_texts.append(button_text)

        while self.response is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, button_rect in enumerate(button_rects):
                        if button_rect.collidepoint(mouse_pos):
                            self.response = options[i]
                            break

            self.screen.fill((0, 0, 0))
            self.screen.blit(text, text_rect)

            for i, button_rect in enumerate(button_rects):
                pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
                button_text_rect = button_texts[i].get_rect(center=button_rect.center)
                self.screen.blit(button_texts[i], button_text_rect)

            pygame.display.flip()
            self.clock.tick(60)

        return self.response  # Return the selected response

    # It is intended to retrieve a snapshot of the current game state.
    def get_game_state_snapshot(self):
        return self.board.fen()

    def restore_game_state(self, fen):
        self.board.set_fen(fen)
        # Update other game state variables if needed

    def record_move(self, move_details):
        # print('move details :', move_details)
        self.move_history.append(move_details)  # Record the move in move_history

    def undo(self):
        if len(self.move_history) > 0:
            last_move = self.move_history.pop()
            self.redo_steps.append(last_move)  # Record the undo step for redo

            # Restore the game state based on the move details
            self.restore_game_state(last_move["game_state"])

    def redo(self):
        if len(self.redo_steps) > 0:
            next_move = self.redo_steps.pop()
            self.move_history.append(next_move)  # Record the redo step in move_history

            # Restore the game state based on the move details
            self.restore_game_state(next_move["game_state"])

    def get_move_details(self, selected_square, target_square):
        move_details = {
            "selected_square": selected_square,
            "target_square": target_square,
            "selected_piece": self.board.piece_at(selected_square),
            "target_piece": self.board.piece_at(target_square),
            "selected_piece_type": None,
        }

        if move_details["selected_piece"]:
            move_details["selected_piece_type"] = move_details["selected_piece"].piece_type

        return move_details

    def handle_mouse_click(self, event):
        if event.button == 1:
            mouse_x, mouse_y = event.pos
            file = int(mouse_x // (self.board_size / 8))
            rank = 7 - int(mouse_y // (self.board_size / 8))
            square = chess.square(file, rank)
            piece = self.board.piece_at(square)

            if piece is not None and piece.color == self.board.turn:
                self.selected_piece = square
                self.valid_moves = self.calculate_valid_moves(square)
                self.target_square = None

            # Display Selected stuff
            elif self.selected_piece is not None:
                self.target_square = square
                move = chess.Move(self.selected_piece, self.target_square)
                move_details = {
                    "move": move,
                    "game_state": self.get_game_state_snapshot()
                }

                if move.to_square in self.valid_moves:
                    if (
                            self.board.piece_at(self.selected_piece).piece_type == chess.PAWN and
                            (chess.square_rank(self.target_square) == 0 or chess.square_rank(self.target_square) == 7)
                    ):
                        print("Selected Piece to Promote:", self.board.piece_at(self.selected_piece))
                        print("Pawn Promotion Occurred")
                        self.perform_pawn_promotion(move)
                    elif (
                            self.board.is_capture(move) and
                            self.board.piece_type_at(move.to_square) == chess.PAWN and
                            (chess.square_rank(self.selected_piece) == 1 or chess.square_rank(self.selected_piece) == 6)
                    ):
                        print("Undoing Pawn Promotion")
                        self.perform_pawn_demotion(move)
                    else:
                        # Store the move details for future undo
                        self.record_move(move_details)
                        # Clear the redo steps
                        self.redo_steps.clear()
                        # Push the move onto the undo stack and update the board
                        self.undo_stack.append(move)
                        self.board.push(move)
                        # Post the custom undo event
                        pygame.event.post(self.undo_event)
                    self.selected_piece = None
                    self.target_square = None

    def perform_pawn_promotion(self, move):
        # Display a pawn promotion dialog and let the player choose a piece
        options = ["Queen", "Rook", "Bishop", "Knight"]  # Add more options if needed
        promotion_piece = self.display_message_with_options("Choose a piece to promote to:", options)

        # Determine the color of the promoted piece
        piece_color = self.board.piece_at(move.from_square).color

        # Determine the promoted piece based on the player's choice
        promoted_piece = None
        if promotion_piece == "Queen":
            promoted_piece = chess.Piece(chess.QUEEN, piece_color)
        elif promotion_piece == "Rook":
            promoted_piece = chess.Piece(chess.ROOK, piece_color)
        elif promotion_piece == "Bishop":
            promoted_piece = chess.Piece(chess.BISHOP, piece_color)
        elif promotion_piece == "Knight":
            promoted_piece = chess.Piece(chess.KNIGHT, piece_color)

        # Remove the original pawn from the board
        self.board.remove_piece_at(move.from_square)

        # Update the board with the promoted piece
        self.board.set_piece_at(move.to_square, promoted_piece)

        # Record move details for pawn promotion
        move_details = {
            "move": move,
            "game_state": self.get_game_state_snapshot()
        }
        self.record_move(move_details)

        # Switch the turn to the opposite player
        self.board.turn = not self.board.turn

        # Update the display
        self.update_display()

    def perform_pawn_demotion(self, move):
        from_square = move.to_square
        to_square = move.from_square

        # Get the promoted piece that needs to be demoted back to a pawn
        promoted_piece = self.board.piece_at(from_square)

        # Determine the original piece color
        piece_color = promoted_piece.color

        # Remove the promoted piece from the board
        self.board.remove_piece_at(from_square)

        # Set the original pawn back to the board
        self.board.set_piece_at(to_square, chess.Piece(chess.PAWN, piece_color))

        # Record move details for pawn demotion
        move_details = {
            "move": move,
            "game_state": self.get_game_state_snapshot()
        }
        self.record_move(move_details)

        # Switch the turn to the opposite player
        self.board.turn = not self.board.turn

        # Update the display
        self.update_display()

    def is_king_checked(self, color):
        king_square = self.board.king(color)
        return self.board.is_attacked_by(not color, king_square)

    def update_display(self):
        self.screen.fill(self.WHITE)

        for row in range(8):
            for col in range(8):
                pygame.draw.rect(
                    self.screen,
                    self.BLACK if (row + col) % 2 == 0 else self.WHITE,
                    pygame.Rect(col * self.board_size / 8, row * self.board_size / 8, self.board_size / 8,
                                self.board_size / 8),
                )

        # Draw file and rank indicators on the edges with customizable width and height
        font_path = pygame.font.match_font('arial')  # You can change 'arial' to another font name
        font = pygame.font.Font(font_path, 20)  # Adjust the font size here

        label_width = 30  # Adjust the width of the labels
        label_height = 30  # Adjust the height of the labels

        for i in range(8):
            file_label = chr(ord('A') + i)  # Use capital letters for files
            rank_label = str((i + 1) + (i >= 8))

            # Draw file indicator on the bottom edge
            file_text_surface = font.render(file_label, True, self.BLACK)
            file_text_rect = file_text_surface.get_rect(center=(
                (i + 0.5) * self.board_size / 8, self.board_size + label_height / 2))  # Adjust the position as needed
            file_text_rect.width = label_width  # Adjust the width of the rectangle
            file_text_rect.height = label_height  # Adjust the height of the rectangle
            self.screen.blit(file_text_surface, file_text_rect)

            # Draw rank indicator on the right edge
            rank_text_surface = font.render(rank_label, True, self.BLACK)
            rank_text_rect = rank_text_surface.get_rect(center=(
                self.board_size + label_width / 2,
                (7 - i + 0.5) * self.board_size / 8))  # Adjust the position as needed
            rank_text_rect.width = label_width  # Adjust the width of the rectangle
            rank_text_rect.height = label_height  # Adjust the height of the rectangle
            self.screen.blit(rank_text_surface, rank_text_rect)

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                piece_with_color = chess.Piece(piece.piece_type, piece.color)  # Create the full piece instance
                piece_image = self.piece_images[piece_with_color]

                piece_rect = piece_image.get_rect(
                    center=(
                        (chess.square_file(square) + 0.5) * self.board_size / 8,
                        (7 - chess.square_rank(square) + 0.5) * self.board_size / 8,
                    )
                )

                # Draw highlighting for checked king
                if piece.piece_type == chess.KING and self.is_king_checked(piece.color):
                    king_file = chess.square_file(square)
                    king_rank = 7 - chess.square_rank(square)
                    king_rect = pygame.Rect(
                        king_file * self.board_size / 8,
                        king_rank * self.board_size / 8,
                        self.board_size / 8,
                        self.board_size / 8,
                    )
                    pygame.draw.rect(self.screen, (255, 10, 10, 10), king_rect, border_radius=5, width=5)

                # Draw highlighting for selected piece
                if square == self.selected_piece:
                    pygame.draw.rect(self.screen, (0, 255, 0, 100), piece_rect, border_radius=5)

                # Draw highlighting for target square
                if square == self.target_square:
                    target_file = self.target_square % 8
                    target_rank = 7 - self.target_square // 8
                    target_rect = pygame.Rect(
                        target_file * self.board_size / 8,
                        target_rank * self.board_size / 8,
                        self.board_size / 8,
                        self.board_size / 8,
                    )
                    pygame.draw.rect(self.screen, (255, 0, 0, 100), target_rect, border_radius=5)

                self.screen.blit(piece_image, piece_rect)

        pygame.display.flip()


if __name__ == "__main__":
    game = ChessGame()
    game.run()
