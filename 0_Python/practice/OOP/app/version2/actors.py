import time
from random import randint


# Z-a
class Character:
    def __init__(self, name, level, hp) -> None:
        self.name = name
        self.level = level
        self.hp = 100 * self.level

    def __repr__(self):
        return f"<Character: {self.name}, level: {self.level}, HP: {self.hp}>"

    def is_alive(self):
        return self.hp > 0

    def get_attack_power(self):
        return randint(1, 100) * self.level

    def attacks(self, target):
        raise NotImplementedError()


# I
class Player(Character):

    # Z-b
    def __init__(self, name, level) -> None:
        super().__init__(name, level, 100)
        self.hp = self.hp + 20

    # Z-c
    def heal(self):
        self.hp += self.level * randint(10, 25)

    # I-2
    def is_attacking(self, enemy):
        damage = self.get_attack_power()
        print(
            f"\n\n{self.name} dealt {damage} damage 💥 to {enemy.name} the {enemy.kind}."
        )
        time.sleep(1)
        enemy.hp -= damage
        print(f"\n\tYour enemy now has {enemy.hp}HP ❤️!\n")
        time.sleep(1.5)


# II
class Enemy(Character):
    def __init__(self, name, level, kind) -> None:
        super().__init__(name, level, 100)
        self.kind = kind

    # I-3
    def is_attacking(self, player):
        damage = self.get_attack_power()
        print(
            f"\n\n{self.name} the {self.kind} dealt {damage} damage 💥 to {player.name}."
        )
        time.sleep(0.5)
        player.hp -= damage
        print(f"\n\tYou are down to {player.hp}HP 💕!\n")
        time.sleep(1)


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
