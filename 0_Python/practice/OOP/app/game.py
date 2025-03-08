import os
import random  # import B
import time

from actors import Enemy, Player  # import A


# I-a
class Game:
    def __init__(self, player, enemies) -> None:
        self.player = player
        self.enemies = enemies

    # G-I
    def main(self):
        # k-a
        os.system("cls" if os.name == "nt" else "clear")
        self.print_intro()
        self.play()

    # I-b
    def print_intro(self):
        print(
            """
        ==== Magic The Quickening ====
        A Super Duper Fast 1 Combat Text Game!
        """
        )
        time.sleep(1)
        print(f"\n\t[Press Enter to Continue]\n\n")
        input()
        # J-a
        time.sleep(0.5)

    # I-e
    def print_linebreaks(self):
        print()
        print("✨" * 30)
        print()

    # I-c
    def play(self):
        while True:
            time.sleep(0.5)
            next_enemy = random.choice(self.enemies)

            # I-d
            cmd = input(f"⚠️  You see a {next_enemy.kind}.\n[r]un, [a]ttack, [p]ass?")
            if cmd == "r":
                time.sleep(0.5)
                print(f"\n{self.player.name} runs away!\n{'💨 '*6}\n\n")
                time.sleep(1)
            elif cmd == "a":
                time.sleep(0.5)
                print(
                    f"\n{self.player.name} swings at {next_enemy.kind}!\n{'⚔️  '*6}\n\n"
                )
                time.sleep(1)

                if self.player.is_attacking(next_enemy):
                    self.enemies.remove(next_enemy)
                    time.sleep(1)
                else:
                    time.sleep(0.5)
                    print(f"{self.player.name} hides to plan the next move ✨\n\n")
                    time.sleep(1)
            elif cmd == "p":
                time.sleep(0.5)
                print(f"\npassing... Plan your next move!\n{'♟️  '*6}\n\n")
                time.sleep(1)
            else:
                print("\n❌ Please choose a valid option")
                time.sleep(0.5)

            # I-j
            # self.print_linebreaks()

            if not self.enemies:
                time.sleep(0.5)
                print(f"You defeated all the enemies!\n")
                time.sleep(0.5)
                print(f"\tCONGRATULATIONS!!!\n")
                print(f"\t{'🎉' * 9}\n\n")
                time.sleep(2)
                # k-a
                os.system("cls" if os.name == "nt" else "clear")
                break


if __name__ == "__main__":
    player = Player(name="Gideon", level=1)
    enemies = [Enemy("Dragon", 1), Enemy("Soldier", 1)]
    Game(player, enemies).main()
