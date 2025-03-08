import time
from random import randint


# I
class Player:
    def __init__(self, name, level) -> None:
        self.name = name
        self.level = level

    # adding a print-out function
    def __repr__(self) -> str:
        return "<Player: {} at Level {}>".format(self.name, self.level)

    # I-1
    def get_attack_power(self):
        return randint(1, 100) * self.level

    # I-2
    def is_attacking(self, enemy):
        damage = self.get_attack_power()
        enemy_damage = enemy.get_attack_power()

        print(f"You dealt {damage} damage 💥.")
        time.sleep(1)
        print(f"{enemy.kind} dealt {enemy_damage} damage! 🩹")
        time.sleep(1.5)

        if damage >= enemy_damage:
            print(f"\n\tYou are victorious! 💪\n\n")
            return True
        else:
            time.sleep(1)
            print(f"\tNo...! {enemy.kind} defeated you! 💔\n\n")


# II
class Enemy:
    def __init__(self, kind, level) -> None:
        self.kind = kind
        self.level = level

    def __repr__(self) -> str:
        return "<Enemy: {} at lvl {}>".format(self.kind, self.level)

    # II-1
    def get_attack_power(self):
        return randint(1, 100) * self.level


if __name__ == "__main__":
    # A1
    player_1 = Player(name="Chandra", level=1)
    ogre_1 = Enemy(kind="Ogre", level=1)
    print(player_1, ogre_1)
    print(player_1.get_attack_power())
    # A1b
    print(ogre_1.get_attack_power())
