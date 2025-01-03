import pygame, sys, chess, math, eval, time
import functions

if __name__ == "__main__":
    pygame.init()

    images = functions.load_images()

    col_conv = {functions.BLACK: chess.BLACK, functions.WHITE: chess.WHITE}
    selected_square = (-1, -1)
    selected_piece = None
    running = True
    functions.draw_chessboard()
    print(eval.maps)
    print(functions.board.piece_map())

    while running:
        functions.render_board_from_fen(functions.board.fen())

        if functions.board.turn == col_conv[functions.BOT_COL]:
            start = time.time()
            _, move = eval.minmax(functions.board, 5, False)
            end = time.time()
            if type(move) is bool:
                print(
                    f"Game over due to {functions.board.outcome().termination}: {functions.board.outcome().result}\nWinner: {functions.board.outcome().winner}"
                )

            print(f"Move made in {end-start} seconds.")
            print(type(move))
            if functions.try_and_push_move(move):
                print("Black played the move ", move.uci())

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                col = max(
                    min((mouse_x - functions.OFFSET) // functions.SQUARE_SIZE, 7), 0
                )
                row = max(
                    min((mouse_y - functions.OFFSET) // functions.SQUARE_SIZE, 7), 0
                )

                if 0 <= col < functions.COLS and 0 <= row < functions.ROWS:
                    if selected_square == (-1, -1):
                        selected_square = (row, col)
                        selected_piece = functions.board.piece_at(
                            chess.square(col, 7 - row)
                        )
                        if (
                            selected_piece is not None
                            and (
                                (
                                    str(selected_piece).isupper() & functions.board.turn
                                    == chess.WHITE
                                )
                                | (
                                    str(selected_piece).islower() & functions.board.turn
                                    == chess.BLACK
                                )
                            )
                            and functions.board.turn == col_conv[functions.PLAYER_COL]
                        ):
                            print(f"Square: {chess.square(col,7-row)}")
                            print(
                                f"Piece: {functions.board.piece_at(chess.square(col,7-row))}"
                            )
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

                        selected_square = (-1, -1)

                print(f"Clicked at row {row}, col {col}!")

            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()
