import pygame, sys, chess, math, eval
import functions

pygame.init()


images = functions.load_images()


selected_square = (-1, -1)
selected_piece = None
running = True
functions.draw_chessboard()
print(eval.maps)
print(functions.board.piece_map())
while running:
    functions.render_board_from_fen(functions.board.fen())
    if functions.board.turn == chess.BLACK:
        move = eval.minmax(functions.board,3,False)[1]
        print(type(move))
        if functions.try_and_push_move(move):
            print("Black played the move ", move.uci())
    

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            col = max(min((mouse_x - functions.OFFSET) // functions.SQUARE_SIZE, 7), 0)
            row = max(min((mouse_y - functions.OFFSET) // functions.SQUARE_SIZE, 7), 0)

            if 0 <= col < functions.COLS and 0 <= row < functions.ROWS:
                if selected_square == (-1, -1):
                    selected_square = (row, col)
                    selected_piece = functions.board.piece_at(chess.square(col, 7 - row))
                    if selected_piece is not None and str(selected_piece).isupper() and functions.board.turn == chess.WHITE:
                        print(f"Square: {chess.square(col,7-row)}")
                        print(f"Piece: {functions.board.piece_at(chess.square(col,7-row))}")
                        functions.highlight_legal_moves(selected_square)
                    pygame.display.update()
                else:
                    rank, file = selected_square
                    move = chess.Move(
                        chess.square(file, 7 - rank), chess.square(col, 7 - row)
                    )
                    if not functions.try_and_push_move(move):
                        selected_square = (-1, -1)
                        functions.draw_chessboard()
                        functions.render_board_from_fen(functions.board.fen())

                    color = functions.WHITE if (row + col) % 2 == 0 else functions.BLACK
                    
                    selected_square = (-1, -1)

            print(f"Clicked at row {row}, col {col}!")

        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
