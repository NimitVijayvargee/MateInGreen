import pygame, chess, sys

WIDTH, HEIGHT = 1000, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = 80
OFFSET = 80
WHITE = (235, 236, 208)
BLACK = (119, 149, 86)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")
board = chess.Board()


def load_images():
    pieces = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
    images = {}
    for piece in pieces:
        images[piece] = pygame.image.load(f"assets/{piece}.png")
    return images


images = load_images()


def draw_chessboard():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (70, 70, 660, 660))
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(
                screen,
                color,
                (
                    col * SQUARE_SIZE + OFFSET,
                    row * SQUARE_SIZE + OFFSET,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                ),
            )


def render_piece(position, piece_type):
    row, col = position
    piece_key = f"{piece_type[0]}{piece_type[1]}"
    piece_image = images[piece_key]
    screen.blit(piece_image, (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET))


def find_king_position(color):
    king_square = board.king(color)
    if king_square is not None:
        return chess.square_name(king_square)
    return None


def is_in_check_or_checkmate():
    color = board.turn
    king_position = find_king_position(color)

    if king_position:
        if board.is_check():
            if board.is_checkmate():
                print(f"Checkmate! {chess.COLOR_NAMES[color]} king at {king_position}")
                pygame.quit()
                sys.exit()

            else:
                pygame.draw.rect(
                    screen,
                    (240, 120, 120),
                    (
                        (board.king(color) % 8) * SQUARE_SIZE + OFFSET,
                        (7 - (board.king(color) // 8)) * SQUARE_SIZE + OFFSET,
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                    ),
                )
        else:
            print(f"King is safe at {king_position}")
    else:
        print(f"King not found on the board.")


def render_board_from_fen(fen):
    piece_mapping = {
        "r": ("b", "r"),
        "n": ("b", "n"),
        "b": ("b", "b"),
        "q": ("b", "q"),
        "k": ("b", "k"),
        "p": ("b", "p"),
        "R": ("w", "r"),
        "N": ("w", "n"),
        "B": ("w", "b"),
        "Q": ("w", "q"),
        "K": ("w", "k"),
        "P": ("w", "p"),
    }

    rows = fen.split(" ")[0].split("/")
    for row_idx, row in enumerate(rows):
        col_idx = 0
        for char in row:
            if char.isdigit():
                col_idx += int(char)
            else:
                render_piece((row_idx, col_idx), piece_mapping[char])
                col_idx += 1


def highlight_legal_moves(screen, board, selected_square, SQUARE_SIZE, OFFSET):
    legal_moves = board.legal_moves
    selected_piece_square = chess.square(selected_square[1], 7 - selected_square[0])

    for move in legal_moves:
        if move.from_square == selected_piece_square:
            dest_square = move.to_square
            col = chess.square_file(dest_square)
            row = 7 - chess.square_rank(dest_square)
            pygame.draw.circle(
                screen,
                (50, 205, 50),
                (
                    col * SQUARE_SIZE + OFFSET + SQUARE_SIZE // 2,
                    row * SQUARE_SIZE + OFFSET + SQUARE_SIZE // 2,
                ),
                SQUARE_SIZE * 0.3,
            )

    pygame.display.update()


if __name__ == "__main__":
    import index
