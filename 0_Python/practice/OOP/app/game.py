import random  # import B

from actors import Enemy, Player  # import A


# G-I
def main():
    print_intro()
    play()


def print_intro():
    print(
        """
    ==== Magic The Quickening ====
    A Super Duper Fast 1 Combat Text Game!
    
        [Press Enter to Continue]
    """
    )
    input()


# G-Ib
def play():
    enemies = [Enemy("Bear", 1), Enemy("Wurm", 1)]
    player = Player("Jace", 1)

    # G-Ic
    while True:
        next_enemy = random.choice(enemies)
        cmd = input(f"You see a {next_enemy.kind}.\n[r]un, [a]ttack, [p]ass?")

        if cmd == "r":
            print(f"\n{player.name} runs away!")
        elif cmd == "a":
            print(f"\n{player.name} swings at {next_enemy.kind}!")

            # G-Ie
            if player.is_attacking(next_enemy):
                enemies.remove(next_enemy)
            else:
                print(f"{player.name} hides to plan the next move")

        elif cmd == "p":
            print(f"\npassing... Plan your next move!")
        # G-Id
        else:
            print("\nPlease choose a valid option")

        print()
        print("*" * 40)
        print()

        # G-J
        if not enemies:
            print("You defeated all the enemies!\n\tCONGRATULATIONS!!!")
            break


if __name__ == "__main__":
    main()
