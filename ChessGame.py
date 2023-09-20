import traceback
import tkinter as tk
import pygame
import chess
import chess.engine
import chess.svg
import re
import datetime


class ChessGame:
    def __init__(self):
        self.game_running = True  # Flag to track whether the game is running

        # Create an instance of the InfoPreview class
        self.info_preview = InfoPreview(self)

        # Create an instance of the Hint class and pass the InfoPreview instance
        self.hint = Hint(self, self.info_preview)

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

        # Create an instance of the OptionDialog class
        self.option_dialog = OptionDialog()

        self.WHITE = (239, 223, 197)
        self.BLACK = (90, 61, 41)

        self.current_player = None

        self.board = chess.Board()
        self.selected_piece = None
        self.target_square = None
        self.response = None

        self.selected_option = None
        self.valid_moves = []
        self.responseAcknowledge = False
        print("Step Condition True")

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
        self.target_square = None
        self.response = None
        self.selected_option = None
        self.responseAcknowledge = False
        self.move_history = []
        self.valid_moves = []  # Store valid moves for the selected piece
        self.undo_stack = []
        self.redo_stack = []
        self.redo_steps = []

        self.info_preview.count = 0
        # ... other game state variables ...

    def get_piece_at_square(self, row, col):
        square = chess.square(col, 7 - row)  # Convert to chess notation (row 0 is the bottom row in Pygame)
        piece = self.board.piece_at(square)
        return piece

    def initialize_board(self):
        print("👉   Board Initializing")
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
        print(f"👉   [{self.info_preview.AtNow()}] Restart the Game")
        # Reset any necessary game state or variables here
        # For example, reset the board, player positions, or any relevant game data
        self.initialize_game()
        self.initialize_board()
        pygame.font.init()  # Initialize Pygame's font module

        # You might also need to reinitialize any UI elements or assets
        # For example, if you display a board, reinitialize it with starting positions

        # Clear the selected option from the previous game over screen
        self.selected_option = None

        # Resume the game loop
        self.run()

    def run(self):
        try:
            while self.game_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_game()  # Call the quit_game method to exit the game
                        self.info_preview.StateArrange("Abandoned")

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_mouse_click(event)

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL:  # Ctrl + Z for Undo
                            self.undo()

                        elif event.key == pygame.K_y and event.mod & pygame.KMOD_CTRL:  # Ctrl + Y for Redo
                            self.redo()

                        elif event.key == pygame.K_h:  # Press 'H' for Hint
                            self.hint.handle_hint()  # Call the hint method

                        # Check for resignation
                        elif event.key == pygame.K_r:
                            self.resign()

                self.update_display()

                if not self.responseAcknowledge:
                    if self.board.is_game_over():
                        if self.board.is_checkmate():
                            winner = ("white" if self.board.turn == chess.BLACK else "black")
                            options = ["Restart", "Exit"]
                            self.info_preview.StateArrange("Check Mate", player=winner.capitalize())

                            self.response = (self.option_dialog.display_message_with_options(
                                f"{winner.capitalize()} player won!", '', options))

                        elif self.board.is_fivefold_repetition():
                            options = ["Restart", "Exit"]
                            self.info_preview.StateArrange("Drawn")

                            self.response = (self.option_dialog.display_message_with_options(
                                "Match Drawn !", "Fivefold Repetition", options))

                        elif self.board.is_stalemate():
                            stalemated = ("Black" if self.board.turn == chess.BLACK else "White")
                            options = ["Restart", "Exit"]
                            self.info_preview.StateArrange("Stalemate")

                            self.response = (self.option_dialog.display_message_with_options(
                                "Match Drawn",
                                f"{stalemated} Stalemate !",
                                options))

                        elif self.board.is_insufficient_material():
                            options = ["Restart", "Exit"]  # You can add more options here if needed
                            self.info_preview.StateArrange("ins_met")

                            self.response = self.option_dialog.display_message_with_options(
                                f"Match Drawn ! ", "Insufficient Material", options)

                        elif self.board.is_fifty_moves():
                            options = ["Restart", "Exit"]  # You can add more options here if needed
                            self.info_preview.StateArrange("fifty_moves")

                            self.response = self.option_dialog.display_message_with_options(
                                "Match Drawn ! ", "Fifty Moves", options)

                        if self.response == "Cancel":
                            self.responseAcknowledge = True
                            self.selected_piece = None

                        # You can then check the response and take appropriate actions based on the player's choice
                        self.GameStatus()

                elif self.selected_piece or self.target_square:
                    self.responseAcknowledge = False
                else:
                    pass

            pygame.quit()

        except Exception as e:
            print("Error: ", e)
            print(traceback.format_exc())

    def quit_game(self):
        if self.hint:
            self.hint.close_engine()  # Close the engine before exiting
        self.game_running = False  # Set the flag to exit the game

    def resign(self):
        resigned_player = "black" if self.board.turn == chess.BLACK else "white"
        winner = "White" if resigned_player == "black" else "Black"
        options = ["Restart", "Exit"]  # You can add more options here if needed
        self.response = self.option_dialog.display_message_with_options("Resigned", f"{winner} player Won !", options)

        if self.response != "Cancel":
            self.info_preview.StateArrange("resign", player=resigned_player)

        self.GameStatus()

    def GameStatus(self):
        if self.response == "Restart":
            self.restart_game()
        elif self.response == "Exit":
            self.quit_game()
        else:
            self.run()

    # It is intended to retrieve a snapshot of the current game state.
    def get_game_state_snapshot(self):
        return self.board.fen()

    def restore_game_state(self, fen):
        self.board.set_fen(fen)
        # Update other game state variables if needed

    def record_moved(self, move_details):
        self.move_history.append(move_details)  # Record the move in move_history

    def record_to_move(self, lst_move):
        self.redo_steps.append(lst_move)

    def undo(self):
        if len(self.undo_stack) > 0:
            current_game_state = self.get_game_state_snapshot()
            self.redo_stack.append(current_game_state)  # Push the current game state onto redo stack
            restored_game_state = self.undo_stack.pop()
            self.restore_game_state(restored_game_state)

            last_move = self.move_history.pop()
            self.record_to_move(last_move)

            self.info_preview.moveDetails(last_move['move'], pieceAct="undone")
        else:
            pass

    def redo(self):
        if len(self.redo_stack) > 0:
            current_game_state = self.get_game_state_snapshot()
            self.undo_stack.append(current_game_state)  # Push the current game state onto undo stack
            restored_game_state = self.redo_stack.pop()
            self.restore_game_state(restored_game_state)

            next_move = self.redo_steps.pop()
            self.record_moved(next_move)

            self.info_preview.moveDetails(next_move['move'], pieceAct="redone")
        else:
            pass

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

                if move.to_square in self.valid_moves:
                    # Check for pawn promotion or not
                    if (
                            self.board.piece_at(self.selected_piece).piece_type == chess.PAWN and
                            (chess.square_rank(move.to_square) == 0 or chess.square_rank(move.to_square) == 7)
                    ):
                        self.perform_pawn_promotion(move)
                    else:
                        # Check if the move is legal based on standard chess rules
                        if self.board.is_legal(move):

                            if self.board.is_castling(move):
                                self.info_preview.moveDetails(move, self.board.piece_at(self.selected_piece),
                                                              pieceAct="Castle")
                            else:
                                self.info_preview.moveDetails(move, self.board.piece_at(self.selected_piece))

                            # Store the current game state for undo
                            self.undo_stack.append(self.get_game_state_snapshot())

                            move_details = {
                                "move": move,
                                "game_state": self.get_game_state_snapshot()
                            }
                            # Store the move details for future undo
                            self.record_moved(move_details)

                            self.info_preview.capturedDetector(move)

                            self.board.push(move)

                            # Post the custom undo event
                            pygame.event.post(self.undo_event)
                        else:
                            print("Illegal move: Standard chess rules violation")
                    self.selected_piece = None
                    self.target_square = None

    def perform_pawn_promotion(self, move):
        # Display a pawn promotion dialog and let the player choose a piece
        options = ["Queen", "Rook", "Bishop", "Knight"]  # Add more options if needed
        self.option_dialog.response = None  # Reset the response attribute
        promotion_piece = self.option_dialog.display_message_with_options("Pawn Promotion", "Promote to", options)

        if promotion_piece:
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
            else:
                pass

            if promoted_piece is not None:
                self.info_preview.moveDetails(move, self.board.piece_at(self.selected_piece), pieceAct=promoted_piece)
                self.info_preview.capturedDetector(move)

                # Store the current game state for undo
                self.undo_stack.append(self.get_game_state_snapshot())

                # Remove the original pawn from the board
                self.board.remove_piece_at(move.from_square)

                # Update the board with the promoted piece
                self.board.set_piece_at(move.to_square, promoted_piece)

                # Record move details for pawn promotion
                move_details = {
                    "move": move,
                    "game_state": self.get_game_state_snapshot()
                }
                self.record_moved(move_details)

                # Switch the turn to the opposite player
                self.board.turn = not self.board.turn

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

                self.screen.blit(piece_image, piece_rect)

            # Highlight the target square (if it exists)
            if square == self.target_square:
                target_file = self.target_square % 8
                target_rank = 7 - self.target_square // 8
                target_rect = pygame.Rect(
                    target_file * self.board_size / 8,
                    target_rank * self.board_size / 8,
                    self.board_size / 8,
                    self.board_size / 8,
                )
                pygame.draw.rect(self.screen, (10, 10, 255, 10), target_rect, border_radius=5, width=5)

        pygame.display.flip()


class Hint:
    def __init__(self, chess_game, info_preview):
        self.chess_game = chess_game
        self.info_preview = info_preview  # Pass the InfoPreview instance
        self.engine = None
        self.closing_engine = False  # Flag to indicate engine closure

        try:
            # Configure the Stockfish engine
            # Path to your Stockfish executable
            self.engine_path = "src_files/stockfish/stockfish-windows-x86-64-avx2.exe"
            self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
            self.configure_stockfish()
            print("[+] Stockfish Engine Activated !")
        except FileNotFoundError as e:
            print(f"Error: Stockfish executable not found at {self.engine_path}\n{e}")
            self.engine = None  # Set engine to None to handle this case

    def configure_stockfish(self):
        # Set Stockfish options using UCI commands
        self.engine.configure({"Skill Level": 10})  # Example option, adjust as needed

    def get_hint(self):
        if self.chess_game.board.is_game_over():
            print("Game is already over. No hints available.")
            return None, None  # Return None values for move and target square

        # Get the best move from the Stockfish engine
        result = self.engine.analyse(self.chess_game.board, chess.engine.Limit(time=2.0))
        best_move = result.get("pv", [])[0] if result.get("pv") else None

        if best_move:
            # Determine the target square from the move
            target_square = best_move.to_square
            return best_move, target_square
        else:
            return None, None

    def handle_hint(self):
        try:
            best_move, target_square = self.get_hint()
            if best_move:
                # Highlight the suggested move and target square
                self.chess_game.selected_piece = best_move.from_square

                # Suggested Details Preview
                self.info_preview.moveDetails(best_move.uci(),
                                              self.chess_game.board.piece_at(self.chess_game.selected_piece),
                                              pieceAct="Suggested")

                self.chess_game.target_square = target_square
                self.chess_game.selected_option = None  # Clear the selected_option

                # Update the display
                self.chess_game.update_display()

                if self.closing_engine:
                    self.close_engine()  # If the engine is closing, trigger engine closure

        except chess.IllegalMoveError as e:
            print("Illegal move suggested by the engine:", e)

    def close_engine(self):
        if self.engine:
            self.closing_engine = True  # Set the flag to indicate engine closure
            self.engine.quit()
            print("[-] Stockfish Engine Quit !")


class OptionDialog:
    def __init__(self):
        self.response = None
        self.dialog = None  # Initialize dialog attribute

        self.dragging = False
        self.start_x = 0
        self.start_y = 0

    def option_clicked(self, option):
        self.response = option
        self.dialog.destroy()

    def on_mouse_press(self, event):
        self.dragging = True
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_release(self, _event):
        self.dragging = False

    def on_mouse_motion(self, event):
        if self.dragging:
            x = self.dialog.winfo_x() + (event.x - self.start_x)
            y = self.dialog.winfo_y() + (event.y - self.start_y)
            self.dialog.geometry(f"+{x}+{y}")

    def buttonDesign(self, text, command):
        button = tk.Button(
            self.dialog,
            text=text,
            command=command,
            padx=10,
            pady=6,
            width=10,
            height=1,
            fg="white",
            bg="#007ACC",  # Background color
            relief="flat",  # Flat border
            font=("Arial", 10, "bold"),  # Custom font
        )

        button.bind("<Enter>", lambda event, b=button: self.on_button_hover(b, True))
        button.bind("<Leave>", lambda event, b=button: self.on_button_hover(b, False))

        return button

    @staticmethod
    def on_button_hover(button, is_hovering):
        if is_hovering:
            button.config(bg="#005999")  # Darker color on hover
        else:
            button.config(bg="#007ACC")  # Original color on leave

    def display_message_with_options(self, message, descr, options):
        root = tk.Tk()
        root.withdraw()  # Hide the main Tkinter window

        self.dialog = tk.Toplevel(root)  # Create and assign the dialog attribute
        self.dialog.overrideredirect(True)  # Remove decorations, including title bar
        self.dialog.geometry("350x320+800+500")

        # Set a dark background color (you can change the color code as needed)
        self.dialog.configure(bg="#2E2E2E")

        # Set transparency (0 = fully transparent, 1 = fully opaque)
        self.dialog.attributes("-alpha", 0.9)  # Adjust the value for the desired level of transparency

        # Close button
        close_button = tk.Button(self.dialog, text="X", command=lambda: self.option_clicked("Cancel"), bg="#2E2E2E",
                                 fg="#FB6400", width=3, height=2, bd=0, activebackground='red')
        close_button.place(x=self.dialog.winfo_reqwidth() + 110, y=10)  # Adjust the position as needed

        lbl_1 = tk.Label(self.dialog, text=message, font=(None, 20), bg="#2E2E2E", fg="white")
        lbl_1.pack(pady=10)

        lbl_2 = tk.Label(self.dialog, text=descr, font=(None, 8), bg="#2E2E2E", fg="silver")
        lbl_2.pack(pady=10)

        for option in options:
            button = self.buttonDesign(option, lambda opt=option: self.option_clicked(opt))
            button.pack(pady=5)

        # Bind mouse events for moving the dialog
        self.dialog.bind("<ButtonPress-1>", self.on_mouse_press)
        self.dialog.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.dialog.bind("<B1-Motion>", self.on_mouse_motion)

        self.dialog.wait_window(self.dialog)

        return self.response


class InfoPreview:
    def __init__(self, chess_game):
        self.chessGame = chess_game
        self.count = 0

    @staticmethod
    def AtNow():
        return datetime.datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def TimeNow():
        return datetime.datetime.now()

    @staticmethod
    def pieceFind(pieceFig):
        if pieceFig.piece_type == chess.PAWN:
            pieceType = "Pawn"
        elif pieceFig.piece_type == chess.KING:
            pieceType = "King"
        elif pieceFig.piece_type == chess.QUEEN:
            pieceType = "Queen"
        elif pieceFig.piece_type == chess.ROOK:
            pieceType = "Rook"
        elif pieceFig.piece_type == chess.BISHOP:
            pieceType = "Bishop"
        else:
            pieceType = "Knight"

        if pieceFig.color:
            pieceColor = "White"
        else:
            pieceColor = "Black"

        return f"{pieceColor} {pieceType}"

    def moveDetails(self, moveAt, pieceFigure=None, pieceAct=None):
        PieceAction = pieceAct

        moving = re.findall(r'[a-zA-Z]+\d+', str(moveAt))

        if pieceFigure is not None:
            self.count += 1
            movedPiece = self.pieceFind(pieceFigure)
            if PieceAction is None:
                print(f"{str(self.count).ljust(4)} [{self.AtNow()}] {movedPiece} Moved from {moving[0]} to {moving[1]}")
            elif PieceAction == "Suggested":
                print(f"     [{self.AtNow()}] Suggested: {movedPiece} Move from {moving[0]} to {moving[1]}")
            elif PieceAction == "Castle":
                print(f"{str(self.count).ljust(4)} [{self.AtNow()}] {movedPiece} Move from {moving[0]} to {moving[1]}"
                      f" & Castled")
            else:
                print(f"{str(self.count).ljust(4)} [{self.AtNow()}] {movedPiece} Moved from {moving[0]} to {moving[1]}"
                      f" & Got a Promotion as a {self.pieceFind(PieceAction)}")

        elif PieceAction == "undone":
            self.count -= 1
            print(f"[{self.AtNow()}] Undo Moved from {moving[1]} to {moving[0]}")
        elif PieceAction == "redone":
            self.count += 1
            print(f"[{self.AtNow()}] Redo Moved from {moving[0]} to {moving[1]}")
        else:
            pass

    def capturedDetector(self, move):
        # Detect if a piece is captured
        captured_piece = self.chessGame.board.piece_at(move.to_square)
        if captured_piece:
            print(f"     [{self.AtNow()}] "
                  f"{self.pieceFind(self.chessGame.board.piece_at(self.chessGame.selected_piece))} "
                  f" captures {self.pieceFind(self.chessGame.board.piece_at(move.to_square))}")

        elif self.chessGame.board.is_en_passant(move):
            captured_pawn = "White" if self.chessGame.board.turn == chess.BLACK else "Black"
            print(f"     [{self.AtNow()}] Pawn En Passant [{captured_pawn} Pawn Captured]")
        else:
            pass

    def StateArrange(self, position, player=None):
        if position == "Abandoned":
            print(f"👉   [{self.AtNow()}] Game {position}")
        elif position == "Drawn":
            print(f"👉   [{self.AtNow()}] Match {position} - Fivefold Repetition")
        elif position == "ins_met":
            print(f"👉   [{self.AtNow()}] Insufficient Material - Match Drawn !")
        elif position == "fifty_moves":
            print(f"👉   [{self.AtNow()}] Fifty Moves - Match Drawn !")
        elif position == "Check Mate":
            print(f"👉   [{self.AtNow()}] {position} & {player} Player Won the Game")
        elif position == "Stalemate":
            print(f"👉   [{self.AtNow()}] {position} !")
        elif position == "resign":
            print(f"👉   [{self.AtNow()}] {player} Player Resigned")
        else:
            pass
        print(f"👉   Total Steps : {self.count}")


if __name__ == "__main__":
    game = ChessGame()
    print(f"| {game.info_preview.TimeNow()} |")
    start = game.info_preview.TimeNow()
    print(f"[{start.time()}] Game Start")
    game.run()
    stop = game.info_preview.TimeNow()
    print(f"[{stop.time()}] Game Stop")

    due = stop - start
    print(f"Total Time : {due}")
