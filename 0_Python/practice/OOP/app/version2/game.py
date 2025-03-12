import os
import random  # import B
import time

from actors import Dragon, Enemy, Player, Soldier  # import A


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

    # Z-5

    def combat(self, next_enemy):
        self.player.is_attacking(next_enemy)
        if not next_enemy.is_alive():
            self.enemies.remove(next_enemy)
            print(f"\nYou defeated the {next_enemy.kind}!\n")
            time.sleep(0.5)
            return

        next_enemy.is_attacking(self.player)
        if not self.player.is_alive():
            print(
                f"\n\n\nNooooOOOO!!😱 😱 😱\n{time.sleep(0.5)}{self.player.name} horribly dies of a horrible life-ending annoying death...!\n"
            )
            time.sleep(0.5)
            print(f"R.I.P {'💀 '*6}\n\n")
            return

        if enemies and self.player.is_alive():
            while next_enemy.is_alive():
                cmd = input(
                    f"The {next_enemy.kind} is till breathing.\n[r]un, [a]ttack?"
                )

                if cmd == "a":
                    # Z-6
                    os.system("cls" if os.name == "nt" else "clear")
                    self.player.is_attacking(next_enemy)
                    if not next_enemy.is_alive():
                        self.enemies.remove(next_enemy)
                        print(f"\nYou defeated the {next_enemy.kind}!\n")
                        time.sleep(0.5)
                        break

                    next_enemy.is_attacking(self.player)
                    if not self.player.is_alive():
                        print(
                            f"\n\n\nNooooOOOO!!😱 😱 😱\n{time.sleep(0.5)}{self.player.name} horribly dies of a horrible life-ending annoying death...!\n"
                        )
                        time.sleep(0.5)
                        print(f"R.I.P {'💀 '*6}\n\n")
                        break

                elif cmd == "r":
                    time.sleep(0.5)
                    print(f"\n{self.player.name} runs away!\n{'💨 '*6}\n\n")
                    time.sleep(1)
                    break

                elif cmd == "h":
                    print(
                        f"\nUnfortunately, you cannot heal during combat\n{' 😢'*6}\n\n"
                    )
                    time.sleep(1)
                else:
                    print("\n❌ Please choose [a]ttack or [r]un.\n")
                    time.sleep(0.5)
            else:
                pass

    # I-c
    def play(self):
        while True:
            if not self.player.is_alive():
                break
            else:
                pass

            # If no enemies left, break
            if not self.enemies:
                break

            # Pick an enemy (only once per loop, or whenever you want a new enemy)
            next_enemy = random.choice(self.enemies)

            time.sleep(0.5)

            cmd = input(f"⚠️  You see a {next_enemy.kind}.\n[r]un, [a]ttack, [h]eal?")
            if cmd == "r":
                time.sleep(0.5)
                print(f"\n{self.player.name} runs away!\n{'💨 '*6}\n\n")
                time.sleep(1)

            # Z-4
            elif cmd == "a":
                time.sleep(0.5)
                self.combat(next_enemy)
                time.sleep(1)

            # Z-3
            elif cmd == "h":
                time.sleep(0.5)
                hp_bef = self.player.hp
                self.player.heal()
                hp_recov = abs(self.player.hp - hp_bef)
                print(
                    f"\nhealing {hp_recov}HP... Your HP is now {self.player.hp}\n{'❤️ '*6}\n\n"
                )
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


if __name__ == "__main__":
    player = Player(name="Gideon", level=1)
    enemies = [Dragon("Nicol Bolas", 1, 1), Soldier("Benalish", 1, 1)]
    Game(player, enemies).main()