import chess.pgn

def get_white_winners(input_file, output_file):
    try:
        pgn_in = open(input_file, 'r', encoding='utf-8')
        pgn_out = open(output_file, 'w', encoding='utf-8')

        count_total = 0
        count_saved = 0

        while True:
            game = chess.pgn.read_game(pgn_in)
            if game is None:
                break  # Reached end

            count_total += 1

            result = game.headers.get("Result", "")
            if result != "1-0":
                continue  
            board = game.board()
            is_clean = True

            try:
                for move in game.mainline_moves():
                    if move not in board.legal_moves:
                        is_clean = False
                        print(f"Illegal move in game {count_total}, skipping.")
                        break
                    board.push(move)
            except Exception as e:
                print(f"Error in game {count_total}: {e}")
                continue

            if is_clean:
                pgn_out.write(str(game) + "\n\n")
                count_saved += 1

        print(f"Done! Checked {count_total} games, saved {count_saved} white wins.")

        pgn_in.close()
        pgn_out.close()

    except FileNotFoundError:
        print(f"Oops! File '{input_file}' not found.")
    except Exception as ex:
        print("Unexpected error:", ex)


# Run this part manually for now, no fancy args yet
if __name__ == "__main__":
    get_white_winners("urpgn.pgn", "FilteredWhite.pgn")
