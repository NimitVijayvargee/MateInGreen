import pygame, sys, chess, math, eval
import functions as f

pygame.init()


images = f.load_images()


selected_square = (-1, -1)
selected_piece = None
running = True
f.draw_chessboard()
print(eval.maps)
print(f.board.piece_map())
while running:
    f.render_board_from_fen(f.board.fen())
    if f.board.turn == chess.BLACK:
        move = eval.minmax(f.board,3,False)
        if f.try_and_push_move(move):
            print("Black played the move ", move.uci())
    

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            col = max(min((mx - f.OFFSET) // f.SQUARE_SIZE, 7), 0)
            row = max(min((my - f.OFFSET) // f.SQUARE_SIZE, 7), 0)

            if 0 <= col < f.COLS and 0 <= row < f.ROWS:
                if selected_square == (-1, -1):
                    selected_square = (row, col)
                    selected_piece = f.board.piece_at(chess.square(col, 7 - row))
                    if selected_piece is not None and str(selected_piece).isupper() and f.board.turn == chess.WHITE:
                        print(f"Square: {chess.square(col,7-row)}")
                        print(f"Piece: {f.board.piece_at(chess.square(col,7-row))}")
                        pygame.draw.rect(
                            f.screen,
                            (77, 92, 61),
                            (
                                col * f.SQUARE_SIZE + f.OFFSET,
                                row * f.SQUARE_SIZE + f.OFFSET,
                                f.SQUARE_SIZE,
                                f.SQUARE_SIZE,
                            ),
                        )
                        f.highlight_legal_moves(selected_square)
                    pygame.display.update()
                else:
                    rank, file = selected_square
                    move = chess.Move(
                        chess.square(file, 7 - rank), chess.square(col, 7 - row)
                    )
                    if not f.try_and_push_move(move):
                        selected_square = (-1, -1)

                    color = f.WHITE if (row + col) % 2 == 0 else f.BLACK
                    pygame.draw.rect(
                        f.screen,
                        color,
                        (
                            col * f.SQUARE_SIZE + f.OFFSET,
                            row * f.SQUARE_SIZE + f.OFFSET,
                            f.SQUARE_SIZE,
                            f.SQUARE_SIZE,
                        ),
                    )
                    selected_square = (-1, -1)

            print(f"Clicked at row {row}, col {col}!")

        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
