import time
from random import randint


# Z-a
class Character:
    def __init__(self, name, level) -> None:
        self.name = name
        self.level = level

    def __repr__(self):
        return f"<Character: {self.name}, level: {self.level}>"

    def get_attack_power(self):
        return randint(1, 100) * self.level

    def attacks(self, target):
        raise NotImplementedError()


# I
class Player(Character):

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
class Enemy(Character):
    def __init__(self, name, level, kind) -> None:
        super().__init__(name, level)
        self.kind = kind


# II-1
class Dragon(Enemy):
    def __init__(self, name, level, size) -> None:
        super().__init__(name, level, "Dragon")
        self.size = size

    def get_attack_power(self):
        return randint(20, 50) * (self.size * self.level)


class Soldier(Enemy):
    def __init__(self, name, level, size) -> None:
        super().__init__(name, level, "Soldier")
        self.size = size

    def get_attack_power(self):
        return randint(1, 35) * (self.size * self.level)


if __name__ == "__main__":
    # A1
    player_1 = Player(name="Chandra", level=1)
    ogre_1 = Enemy(kind="Ogre", level=1)
    print(player_1, ogre_1)
    print(player_1.get_attack_power())
    # A1b
    print(ogre_1.get_attack_power())
