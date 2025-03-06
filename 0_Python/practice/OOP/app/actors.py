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
