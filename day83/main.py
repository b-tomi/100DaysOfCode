# Tic Tac Toe Project

from game_engine import GameEngine


def main():
    # possible to change the player's names, or even ask the user to input them
    game = GameEngine(p1_name="Player 1", p2_name="Player 2")
    game.start()

    # main loop
    while True:
        # round loop
        while game.round_in_progress():
            game.print_board()
            game.next_move()

        # condition to break out of main game loop
        print("Do you want to play another round? (y/n)")
        if input("> ").lower() == "n":
            break
        # else start a new round
        game.new_round()

    # print the final score
    game.print_score(final=True)
    print("\nGoodbye.")


if __name__ == "__main__":
    main()
