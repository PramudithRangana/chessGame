import traceback
import pygame
import chess


# noinspection PyAttributeOutsideInit
class ChessGame:
    # Initialization code for setting up the game, creating the game window, loading assets, and more.
    def __init__(self):
        """
        Constructor for initializing the ChessGame instance.

        This method sets up the initial state of the chess game, including the game window,
        assets, fonts, and other relevant variables. It also loads chess piece images, defines
        custom event types, initializes the game board, and more.

        :return: None
        """
        self.move_history = []
        self.BLACK = (0, 0, 0)
        self.screen = None
        self.WHITE = (255, 255, 255)
        self.board_size = None
        self.redo_event = []
        self.piece_images = []
        self.redo_stack = []
        self.undo_stack = []
        pygame.init()  # Initialize Pygame
        pygame.font.init()  # Initialize Pygame's font module

        self.clock = pygame.time.Clock()

        # Calculate the dynamic board size based on the smaller screen dimension
        # ... (code for calculating board size and other screen-related setup) ...

        # Create a larger surface to include space for labels
        # ... (code for creating the game window and surface) ...

        # Define custom event types for undo and redo
        # ... (code for defining custom event types) ...

        # Load chess piece images
        # ... (code for loading chess piece images) ...

        # Initialize font for options
        # ... (code for initializing fonts) ...

        # Set color constants for the board
        # ... (setting up color constants for the chessboard) ...

        # Initialize game state variables
        # ... (setting up game state variables like current_player, selected_piece, etc.) ...

        # Initialize the chess board
        # ... (code for initializing the game board) ...

        # Initialize other game-related variables
        # ... (initialize variables like selected_option, valid_moves, response, etc.) ...

        # Call the run method to start the main game loop
        self.run()

        """
        The __init__ method serves as the constructor of the ChessGame class. It's called when you create an 
        instance of the class. The method sets up various aspects of the game, including the game window, fonts, 
        colors, game state variables, and more. It also initializes game-related assets like chess piece images and 
        defines custom event types for undo and redo actions. Once the initialization is complete, the method calls 
        the run method to start the main game loop, which is responsible for running the game and handling events.
        """

    # Calculate and return valid moves for a selected piece on the board.
    def calculate_valid_moves(self, selected_square):
        """
        Calculate valid moves for the selected piece on the board.

        param selected_square: The square where the selected piece is located.
        return: A list of squares representing valid moves for the selected piece.
        """
        valid_moves = []

        if self.board.piece_at(selected_square):
            # If there's a piece on the selected square, iterate through legal moves.
            for move in self.board.legal_moves:
                if move.from_square == selected_square:
                    # If the move's starting square matches the selected square, it's a valid move.
                    valid_moves.append(move.to_square)

                    # Check if the selected piece is a pawn and can be promoted.
                    if (
                            self.board.piece_at(selected_square).piece_type == chess.PAWN and
                            (chess.square_rank(move.to_square) == 0 or chess.square_rank(move.to_square) == 7)
                    ):
                        # Add options for pawn promotion: queen, rook, bishop, knight.
                        valid_moves.append(move.to_square + chess.QUEEN)
                        valid_moves.append(move.to_square + chess.ROOK)
                        valid_moves.append(move.to_square + chess.BISHOP)
                        valid_moves.append(move.to_square + chess.KNIGHT)

        return valid_moves

    """
    This method calculates valid moves for a selected piece on the chessboard. It iterates through the legal moves 
    for the entire board and checks if the starting square of each move matches the selected square. If it does, 
    the move's ending square is added to the list of valid moves. 

    For pawn pieces, it also considers the possibility of pawn promotion, where a pawn can be promoted to a queen,  
    rook, bishop, or knight when it reaches the opposite end of the board. 

    The method then returns a list of squares representing valid moves for the selected piece.
    """

    # Initialize the game state, including the board, current player, selected piece, valid moves, etc.
    def initialize_game(self):
        """
        Initialize or reset the game state.

        This method resets various game-related variables to their initial values.
        It prepares the board, sets the starting player, and clears any previous selections.

        :return: None
        """
        self.board = chess.Board()  # Initialize the game board as a chess.Board object
        self.current_player = "white"  # Set the starting player
        self.selected_piece = None  # Store the currently selected piece
        self.valid_moves = []  # Store valid moves for the selected piece
        # ... other game state variables ...

    """
    This method is responsible for initializing or resetting the game state. It is called when the game is 
    started initially or when the game needs to be restarted. The method performs the following tasks: 

    It initializes the game board as a chess.Board object, essentially starting a new game.
    It sets the starting player to "white" to indicate that the game begins with the white player's turn.
    It clears any previously selected piece by setting the selected_piece variable to None.
    It clears the list of valid moves by setting the valid_moves list to an empty list.
    Any other relevant game state variables are reset to their initial values as needed.

    In essence, this method ensures that the game starts fresh with the board set up for the initial position, 
    the white player's turn, and no pieces or moves selected. 
    """

    # Get the chess piece at a specific row and column on the board.
    def get_piece_at_square(self, row, col):
        """
        Get the chess piece at a specific row and column on the board.

        param row: The row index of the square (0 to 7).
        param col: The column index of the square (0 to 7).
        return: The chess piece at the specified square or None if no piece is present.
        """
        square = chess.square(col, 7 - row)  # Convert to chess notation (row 0 is the bottom row in Pygame)
        piece = self.board.piece_at(square)
        return piece

    """
    This method takes the row and column indices of a square on the chessboard and returns the chess piece located 
    at that square. It does this by converting the provided row and column indices into a square index using the 
    chess.square() function. It then uses the piece_at() method of the chess.Board object to retrieve the piece 
    present on that square. 

    The method returns the chess piece object if a piece is present on the specified square, or None if no piece is 
    located there. The conversion from row and column indices to the chess square index accounts for the difference in 
    indexing conventions between Pygame (where row 0 is the top row) and the chess library (where row 0 is the bottom 
    row).
    """

    # Create and initialize the graphical representation of the chess board.
    def initialize_board(self):
        """
        Create and initialize the graphical representation of the chess board.

        This method generates a 2D grid representing the chess board and populates it with
        chess piece images based on the current positions of the pieces on the board.

        :return: A 2D grid (list of lists) containing chess piece images for each square.
        """
        board = [[None] * 8 for _ in range(8)]  # Initialize an empty 8x8 grid

        # Iterate through the chessboard squares
        for row in range(8):
            for col in range(8):
                # Get the chess piece at the current square
                piece = self.get_piece_at_square(row, col)  # Implement this function to get the piece for the square

                # If a piece is present, retrieve its corresponding image from the piece_images dictionary
                if piece:
                    board[row][col] = self.piece_images[piece]  # Store the image in the board grid

        return board  # Return the initialized chess board grid

    """
    This method is responsible for creating and initializing the graphical representation of the chess board. It 
    generates a 2D grid (a list of lists) where each element corresponds to a square on the chessboard. If a chess 
    piece is present on a square, the corresponding element in the grid is set to the image of that piece. 

    The method iterates through all the squares on the chessboard, and for each square, it retrieves the corresponding 
    chess piece using the get_piece_at_square method. If a piece is present, it fetches the appropriate image from the 
    piece_images dictionary and stores it in the grid. 
    
    Finally, the method returns the initialized grid, which contains images representing the pieces' positions on the 
    chessboard. This grid is used to display the visual representation of the chessboard in the game window. 
    """

    # Restart the game by resetting the game state, UI, and resuming the game loop.
    def restart_game(self):
        """
        Restart the game by resetting the game state, UI, and resuming the game loop.

        This method resets various game-related variables to their initial values, reinitializes
        the game board and UI elements, clears any previous game over selections, and then resumes
        the main game loop.

        return: None
        """
        # Reset the game state variables and clear any previous selections
        self.initialize_game()

        # Reinitialize the graphical representation of the chess board
        self.initialize_board()

        # Clear the selected option from the previous game over screen
        self.selected_option = None

        # Resume the game loop
        self.run()

    """
    The restart_game method is responsible for restarting the game when requested by the player. It performs the 
    following tasks: 

    It resets various game-related variables to their initial values by calling the initialize_game method. This 
    includes resetting the game board, current player, selected pieces, and valid moves. It reinitializes the 
    graphical representation of the chessboard by calling the initialize_board method. This ensures that the UI is 
    updated to reflect the new game state. It clears the selected_option variable, which might have been set during 
    the game over screen. Finally, it resumes the main game loop by calling the run method, allowing the player to 
    continue playing. 

    In essence, this method provides a way to start a new game with a clean slate, resetting all relevant game variables 
    and UI elements. 
    """

    # Main game loop, handling events, updating the display, and managing game over conditions.
    def run(self):
        try:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Handle mouse clicks on the board.
                        self.handle_mouse_click(event)

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL:
                            # If Ctrl + Z is pressed, undo the last move.
                            self.undo()

                        elif event.key == pygame.K_y and event.mod & pygame.KMOD_CTRL:
                            # If Ctrl + Y is pressed, redo the last undone move.
                            self.redo()

                self.update_display()

                if self.board.is_game_over():
                    # Handle game over when a player is in checkmate.
                    if self.board.is_checkmate():
                        pass
                    # Display options to restart or exit the game.
                    # Handle the player's response accordingly.

                    # Handle game over when the game is a draw due to fivefold repetition.
                    elif self.board.is_fivefold_repetition():
                        pass
                    # Display options to restart or exit the game.
                    # Handle the player's response accordingly.
                    # Handle other game over conditions here, if needed.

                pygame.display.flip()

            pygame.quit()

        except Exception as e:
            print("Error: ", e)
            print(traceback.format_exc())

    # Display a message with multiple options and wait for the player to choose an option.
    def display_message_with_options(self, message, options):
        """
        Display a message to the player along with multiple selectable options.

        This method creates a UI overlay displaying the given message and a list of options.
        The player can click on one of the options, and the method waits until an option is chosen.
        It handles player input events and returns the chosen option when the player makes a selection.

        param message: The message to be displayed to the player.
        param options: A list of selectable options for the player to choose from.
        return: The chosen option selected by the player.
        """
        # ... (code for setting up font, text, and button positions) ...
        button_rects = []
        while self.response is None:
            # Check for player input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the player clicked on one of the buttons
                    mouse_pos = pygame.mouse.get_pos()
                    for i, button_rect in enumerate(button_rects):
                        if button_rect.collidepoint(mouse_pos):
                            self.response = options[i]  # Set the chosen response based on the clicked button
                            break

            # Update the UI overlay
            # ... (code for rendering text and buttons, handling button clicks) ...

            pygame.display.flip()
            self.clock.tick(60)

        return self.response  # Return the player's chosen response

    """
    The display_message_with_options method is responsible for creating a graphical UI overlay that displays a 
    message to the player along with a list of selectable options. It allows the player to click on one of the 
    options and waits until a selection is made. Here's how the method works: 

    The method takes a message to display and a list of options as input parameters. Inside the method, it enters a 
    loop that keeps running until the player makes a selection (self.response is set). The loop checks for player 
    input events (mouse clicks and window close events) using pygame.event.get(). If the player clicks on one of the 
    buttons (options), the method records the clicked option and sets it as the chosen response. The UI overlay is 
    updated based on the current state, including rendering the message and buttons. The game display is updated 
    using pygame.display.flip() and the loop waits to keep the UI responsive. 

    Once the player makes a selection, the method returns the chosen option, which can then be used to determine the 
    player's decision. This method is commonly used to display messages and options during game over screens or when 
    presenting choices to the player. 
    """

    # It is intended to retrieve a snapshot of the current game state.
    def get_game_state_snapshot(self):
        """
        The function returns the current state of the game board in a FEN (Forsyth-Edwards Notation) format. FEN is
        a standard notation for describing a particular board position of a chess game. It includes information
        about piece placement, active color, castling availability, en passant target square, and halfmove and
        full move numbers.
        """
        return self.board.fen()

    def restore_game_state(self, fen):
        self.board.set_fen(fen)
        # Update other game state variables if needed

    def record_move(self, move_details):
        self.move_history.append(move_details)  # Record the move in move_history

    # Undo the last move by popping it from the undo stack and updating the board.
    def undo(self):
        """
        Undo the last move in the game.

        This method allows the player to undo the last move made in the game.
        It removes the last move from the move history, updates the board state,
        and posts a custom redo event to allow for redoing the undone move.

        return: None
        """
        if len(self.undo_stack) > 0:
            # Pop the last move from the undo stack
            last_move = self.undo_stack.pop()

            # Push the undone move to the redo stack
            self.redo_stack.append(last_move)

            # Update the board state by removing the last move
            self.board.pop()

            # Post the custom redo event to allow redoing the undone move
            pygame.event.post(self.redo_event)

    """
    The undo method is responsible for allowing the player to undo the last move made in the game. Here's how the 
    method works: 

    The method checks if there are moves in the undo_stack (move history) to undo. If there are moves to undo, 
    it pops the last move from the undo_stack. The undone move is then pushed onto the redo_stack, which allows the 
    player to redo the undone move if desired. The method updates the game board's state by removing the last move 
    using the pop() method. Finally, a custom redo event is posted using pygame.event.post(self.redo_event). This 
    event informs the game that an undone move is available for redoing. 

    In summary, this method enables the player to undo their last move, stores the undone move for potential redoing, 
    and updates the game state accordingly. 
    """

    # Redo a move by popping it from the redo stack and updating the board.
    def redo(self):
        """
        Redo a previously undone move in the game.

        This method allows the player to redo a previously undone move.
        It retrieves the next move from the redo stack, updates the board state,
        and posts a custom undo event to allow for undoing the redone move.

        :return: None
        """
        if len(self.redo_stack) > 0:
            # Pop the next move from the redo stack
            next_move = self.redo_stack.pop()

            # Push the redone move back onto the undo stack
            self.undo_stack.append(next_move)

            # Update the board state by pushing the redone move
            self.board.push(next_move)

            # Post the custom undo event to allow undoing the redone move
            pygame.event.post(self.undo_event)

    """
    The redo method is responsible for allowing the player to redo a previously undone move in the game. Here's 
    how the method works: 

    The method checks if there are moves in the redo_stack (moves that were undone and stored for redoing). If there 
    are moves to redo, it pops the next move from the redo_stack. The redone move is then pushed back onto the 
    undo_stack, which allows the player to undo the redone move if needed. The method updates the game board's state 
    by pushing the redone move using the push() method. Finally, a custom undo event is posted using 
    pygame.event.post(self.undo_event). This event informs the game that a redone move is available for undoing. 

    In summary, this method enables the player to redo a previously undone move, restores the move to the game history, 
    and updates the game state accordingly. 
    """

    def get_move_details(self, selected_square, target_square):
        """
        Get details about a player's move, including clicked piece, piece type, target piece, and more.

        param selected_square: The square from which the player's piece is moved.
        param target_square: The target square to which the player's piece is moved.
        return: A dictionary containing details about the move.
        """
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

    # Handle mouse clicks by selecting pieces, moving them, and triggering actions based on the game state.
    def handle_mouse_click(self, event):
        """
        Handle mouse clicks during the game.

        This method is responsible for processing player mouse clicks on the chessboard.
        It identifies the source square (selected piece) and the target square (move destination),
        checks the validity of the move, and updates the game state accordingly.

        param event: The mouse click event containing information about the clicked position.
        return: None
        """
        if event.button == 1:  # Left mouse button clicked
            mouse_x, mouse_y = event.pos
            file = int(mouse_x // (self.board_size / 8))  # Convert mouse position to file index
            rank = 7 - int(mouse_y // (self.board_size / 8))  # Convert mouse position to rank index
            square = chess.square(file, rank)  # Convert to chess square notation
            piece = self.board.piece_at(square)  # Get the chess piece at the clicked square

            if piece is not None and piece.color == self.board.turn:
                # If a piece is clicked, and it belongs to the current player's turn
                self.selected_piece = square  # Store the selected piece square
                self.valid_moves = self.calculate_valid_moves(square)  # Calculate valid moves for the selected piece
                self.target_square = None  # Clear the target square

            elif self.selected_piece is not None:
                # If a piece is already selected and a target square is clicked
                self.target_square = square  # Store the target square of the move
                move = chess.Move(self.selected_piece, self.target_square)  # Create a move object

                if move.to_square in self.valid_moves:
                    # If the target square is a valid move for the selected piece
                    if (
                            self.board.piece_at(self.selected_piece).piece_type == chess.PAWN and
                            (chess.square_rank(self.target_square) == 0 or chess.square_rank(self.target_square) == 7)
                    ):
                        # Check for pawn promotion
                        self.perform_pawn_promotion(move)
                    else:
                        # Regular move
                        self.undo_stack.append(move)  # Push the move onto the undo stack
                        self.redo_stack.clear()  # Clear the redo stack
                        self.board.push(move)  # Update the game board state
                        pygame.event.post(self.undo_event)  # Post the custom undo event
                    self.selected_piece = None  # Clear the selected piece
                    self.target_square = None  # Clear the target square
    """
    The handle_mouse_click method is responsible for processing player mouse clicks on the chessboard. It 
    responds to left mouse button clicks and determines the source square (selected piece) and the target square 
    (move destination). Here's how the method works: 

    If the left mouse button is clicked (event.button == 1): It calculates the clicked square's coordinates based on 
    the mouse position and converts them to chess notation. It retrieves the chess piece (if any) located at the 
    clicked square. If a piece is clicked and it belongs to the current player's turn, it stores the selected piece 
    square and calculates the valid moves for that piece. If a piece is already selected and a target square is 
    clicked: It stores the target square for the move. It creates a chess.Move object representing the move from the 
    selected piece to the target square. If the target square is a valid move for the selected piece: If the selected 
    piece is a pawn and the move involves promotion, it calls perform_pawn_promotion to handle the pawn promotion 
    logic. Otherwise, it adds the move to the undo_stack, clears the redo_stack, updates the board state, 
    and posts the custom undo event. Finally, it clears the selected piece and target square to prepare for the next 
    move. 

    In summary, this method manages the player's interactions with the chessboard through mouse clicks, calculates valid 
    moves, handles regular moves and pawn promotions, and updates the game state accordingly 
    """

    # Handle pawn promotion by allowing the player to choose a promoted piece and updating the board.
    def perform_pawn_promotion(self, move):
        """
        Handle the pawn promotion process during a chess move.

        This method is called when a pawn reaches the opposite end of the board and needs to be promoted.
        It displays a dialog allowing the player to choose the piece to promote the pawn to.
        After the player's choice, it updates the board with the promoted piece and switches the turn.

        param move: The move object representing the pawn's move to the promotion square.
        return: None
        """
        # Display a pawn promotion dialog and let the player choose a piece
        options = ["Queen", "Rook", "Bishop", "Knight"]  # List of available promotion options
        promotion_piece = self.display_message_with_options("Choose a piece to promote to:", options)

        # Determine the color of the promoted piece (same as the pawn's color)
        piece_color = self.board.piece_at(move.from_square).color

        # Initialize the promoted_piece variable
        promoted_piece = None

        # Determine the promoted piece based on the player's choice
        if promotion_piece == "Queen":
            promoted_piece = chess.Piece(chess.QUEEN, piece_color)
        elif promotion_piece == "Rook":
            promoted_piece = chess.Piece(chess.ROOK, piece_color)
        elif promotion_piece == "Bishop":
            promoted_piece = chess.Piece(chess.BISHOP, piece_color)
        elif promotion_piece == "Knight":
            promoted_piece = chess.Piece(chess.KNIGHT, piece_color)

        # Push the promotion move onto the undo stack
        self.undo_stack.append(move)
        self.redo_stack.clear()

        # Remove the original pawn from the board
        self.board.remove_piece_at(move.from_square)

        # Update the board with the promoted piece
        self.board.set_piece_at(move.to_square, promoted_piece)

        # Switch the turn to the opposite player
        self.board.turn = not self.board.turn

        # Update the display
        self.update_display()

    """
    The perform_pawn_promotion method handles the process of promoting a pawn to a higher-ranked piece when it 
    reaches the opposite end of the board. Here's how the method works: 

    It displays a dialog using the display_message_with_options method, allowing the player to choose the piece to 
    which the pawn should be promoted (options are "Queen," "Rook," "Bishop," and "Knight"). It determines the color 
    of the promoted piece, which is the same as the color of the pawn being promoted. Based on the player's choice, 
    it determines the piece type of the promoted piece (Queen, Rook, Bishop, or Knight) and initializes the 
    promoted_piece variable accordingly. It adds the original pawn's move (leading to the promotion square) to the 
    undo_stack to preserve the move history. It removes the original pawn from the board using 
    self.board.remove_piece_at(move.from_square). It updates the board with the promoted piece using 
    self.board.set_piece_at(move.to_square, promoted_piece). It switches the turn to the opposite player to continue 
    the game. Finally, it updates the display to reflect the changes in the game board. 

    In summary, this method manages the pawn promotion process, allowing the player to choose a piece and updating the 
    game state accordingly. 
    """

    # Check if the king of a given color is currently in a checked position.
    def is_king_checked(self, color):
        """
        Check if the king of the specified color is in check.

        This method determines if the king of the specified color is under threat (checked).
        It checks whether the opponent's pieces have a legal move to capture the king's square.

        param color: The color of the king to check for (chess.WHITE or chess.BLACK).
        return: True if the king is in check, False otherwise.
        """
        king_square = self.board.king(color)  # Get the square position of the specified color's king
        return self.board.is_attacked_by(not color,
                                         king_square)  # Check if the king's square is attacked by opponent's pieces

    """
    The is_king_checked method is responsible for determining whether the king of a specified color is under 
    threat (in check) by the opponent's pieces. Here's how the method works: 

    The method takes the color of the king to check (chess.WHITE or chess.BLACK) as a parameter. It retrieves the 
    square position of the specified color's king using self.board.king(color). It uses the 
    self.board.is_attacked_by() method to check if the king's square is attacked by any of the opponent's pieces. The 
    not color argument is used to get the opponent's color. If the king's square is attacked, the method returns 
    True, indicating that the king is in check. Otherwise, it returns False. 

    In summary, this method checks whether a king of a specific color is currently in check, which is a critical aspect 
    of chess gameplay.
    """

    # Update the graphical display of the chess board and pieces.
    def update_display(self):
        """
        Update the game display with the current state of the chessboard.

        This method is responsible for refreshing the graphical representation of the chessboard
        based on the current game state. It draws the chessboard, pieces, labels, and highlighting
        to indicate selected and target squares.

        :return: None
        """
        self.screen.fill(self.WHITE)  # Fill the screen with the white color

        # Draw the chessboard squares
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(
                    self.screen,
                    self.BLACK if (row + col) % 2 == 0 else self.WHITE,
                    pygame.Rect(col * self.board_size / 8, row * self.board_size / 8, self.board_size / 8,
                                self.board_size / 8),
                )

        # Draw file and rank indicators on the edges
        font_path = pygame.font.match_font('arial')  # Find a suitable font
        font = pygame.font.Font(font_path, 20)  # Initialize the font and font size

        label_width = 30  # Set the width of the labels
        label_height = 30  # Set the height of the labels

        # Draw file indicators (letters) at the bottom edge of the board
        for i in range(8):
            file_label = chr(ord('A') + i)  # Convert index to capital letter
            file_text_surface = font.render(file_label, True, self.BLACK)  # Render the label text
            file_text_rect = file_text_surface.get_rect(
                center=((i + 0.5) * self.board_size / 8, self.board_size + label_height / 2))
            file_text_rect.width = label_width  # Set the width of the label rectangle
            file_text_rect.height = label_height  # Set the height of the label rectangle
            self.screen.blit(file_text_surface, file_text_rect)  # Blit the label onto the screen

        # Draw rank indicators (numbers) at the right edge of the board
        for i in range(8):
            rank_label = str((i + 1) + (i >= 8))  # Convert index to number
            rank_text_surface = font.render(rank_label, True, self.BLACK)  # Render the label text
            rank_text_rect = rank_text_surface.get_rect(
                center=(self.board_size + label_width / 2, (7 - i + 0.5) * self.board_size / 8))
            rank_text_rect.width = label_width  # Set the width of the label rectangle
            rank_text_rect.height = label_height  # Set the height of the label rectangle
            self.screen.blit(rank_text_surface, rank_text_rect)  # Blit the label onto the screen

        # Draw the pieces on the board
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                # Get the piece image based on the piece type and color
                piece_with_color = chess.Piece(piece.piece_type, piece.color)
                piece_image = self.piece_images[piece_with_color]

                # Calculate the position to draw the piece
                piece_rect = piece_image.get_rect(
                    center=(
                        (chess.square_file(square) + 0.5) * self.board_size / 8,
                        (7 - chess.square_rank(square) + 0.5) * self.board_size / 8,
                    )
                )

    """
    The update_display method is responsible for updating the graphical representation of the chessboard and game 
    elements based on the current game state. Here's how the method works: 

    It fills the entire screen with the white color to clear any previous display.
    It draws the alternating colors of the chess
    """


# Create an instance of the ChessGame class and start the game loop.
if __name__ == "__main__":
    """
    Entry point for the chess game.

    This block of code is executed only if the script is run as the main program (not imported as a module).
    It creates an instance of the `ChessGame` class, initializes the game, and starts the game loop.

    The game loop continues running until the player quits the game or closes the window.
    During each iteration of the loop, player input events are processed, the game state is updated,
    and the display is refreshed to reflect the current state of the game.

    After the game loop exits, Pygame is cleaned up and the program terminates.

    :return: None
    """
    game = ChessGame()  # Create an instance of the ChessGame class
    game.run()  # Start the game loop

    """
    The __name__ == "__main__" block serves as the entry point for the chess game. Here's how the block works:

    It checks whether the script is being executed as the main program (not imported as a module) using the __name__ 
    special variable. If the script is being run as the main program (__name__ is set to "__main__"): It creates an 
    instance of the ChessGame class using game = ChessGame(). It starts the game loop by calling the game.run() 
    method. The game loop handles player input, updates the game state, and refreshes the display. The game loop 
    continues running until the player quits the game or closes the game window. After the game loop exits (when the 
    player decides to quit), the pygame.quit() function is called to clean up the Pygame resources, and the program 
    terminates. 

    In summary, the __name__ == "__main__" block ensures that the game logic and loop are executed only when the script 
    is run as the main program, allowing the chess game to be played and interacted with through the graphical user 
    interface. 
    """
