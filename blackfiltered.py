import chess.pgn

def extract_black_wins(input_filename, output_filename):
    try:
        in_file = open(input_filename, 'r', encoding='utf-8')
        out_file = open(output_filename, 'w', encoding='utf-8')

        total_games = 0
        saved_games = 0

        while True:
            game = chess.pgn.read_game(in_file)
            if game is None:
                break

            total_games += 1

            result = game.headers.get("Result", "")

            if result != "0-1":
                continue

            board = game.board()
            legal_moves = True

            try:
                for move in game.mainline_moves():
                    if move not in board.legal_moves:
                        legal_moves = False
                        print(f"Game {total_games} has illegal move, skipping it...")
                        break
                    board.push(move)
            except Exception as e:
                print(f"Error in game {total_games}: {e}")
                continue

            if legal_moves:
                out_file.write(str(game) + "\n\n")
                saved_games += 1

            if total_games % 50 == 0:
                print(f"Processed {total_games} games so far...")

        print(f"All done! Processed {total_games} games.")
        print(f"Saved {saved_games} games where Black won.")

        in_file.close()
        out_file.close()

    except FileNotFoundError:
        print(f"File '{input_filename}' not found, please check the path!")
    except Exception as e:
        print("Oops, something went wrong:", e)

if __name__ == "__main__":
    # change these
    input_pgn = "ur.pgn"
    output_pgn = "FilteredBlackPgn.pgn"

    extract_black_wins(input_pgn, output_pgn)
