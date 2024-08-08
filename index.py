import pygame, sys, chess, math

pygame.init()
board = chess.Board()
WIDTH, HEIGHT = 1000, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = 80
OFFSET = 80

WHITE = (235, 236, 208)
BLACK = (119, 149, 86)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Board')

def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 
              'bp', 'br', 'bn', 'bb', 'bq', 'bk']
    images = {}
    for piece in pieces:
        images[piece] = pygame.image.load(f'assets/{piece}.png')
    return images

def draw_chessboard():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (70, 70, 660, 660))
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET, SQUARE_SIZE, SQUARE_SIZE))

def render_piece(position, piece_type):
    row, col = position
    piece_key = f'{piece_type[0]}{piece_type[1]}'
    piece_image = images[piece_key]
    screen.blit(piece_image, (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET))

images = load_images()

def render_board_from_fen(fen):
    piece_mapping = {
        'r': ('b', 'r'), 'n': ('b', 'n'), 'b': ('b', 'b'),
        'q': ('b', 'q'), 'k': ('b', 'k'), 'p': ('b', 'p'),
        'R': ('w', 'r'), 'N': ('w', 'n'), 'B': ('w', 'b'),
        'Q': ('w', 'q'), 'K': ('w', 'k'), 'P': ('w', 'p')
    }
    
    rows = fen.split(' ')[0].split('/')
    for row_idx, row in enumerate(rows):
        col_idx = 0
        for char in row:
            if char.isdigit():
                col_idx += int(char)
            else:
                render_piece((row_idx, col_idx), piece_mapping[char])
                col_idx += 1

move = chess.Move.from_uci("e2e4")
if move in board.legal_moves:
    board.push(move)
else:
    print("Illegal move")

selected_squares = []
running = True
draw_chessboard()
while running:
    render_board_from_fen(board.fen())
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            col = max(min((mx - OFFSET) // SQUARE_SIZE, 7),0)
            row = max(min((my - OFFSET) // SQUARE_SIZE, 7),0)
            
            if 0 <= col < COLS and 0 <= row < ROWS:
                if not selected_squares.__contains__((row,col)):
                    
                    selected_squares.append((row,col))
                    pygame.draw.rect(screen, (77, 92, 61), (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET, SQUARE_SIZE, SQUARE_SIZE))
                    pygame.display.update()
                else:
                    color = WHITE if (row + col) % 2 == 0 else BLACK
                    pygame.draw.rect(screen, color, (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET, SQUARE_SIZE, SQUARE_SIZE))
                    selected_squares.pop(selected_squares.index((row,col)))
            print(f"Clicked at row {row}, col {col}!")
            
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()

pygame.quit()
sys.exit()
