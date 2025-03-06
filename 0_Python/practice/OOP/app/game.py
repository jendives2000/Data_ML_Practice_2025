# import A
from actors import Enemy, Player


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

    print(enemies)
    print(player)


if __name__ == "__main__":
    main()
