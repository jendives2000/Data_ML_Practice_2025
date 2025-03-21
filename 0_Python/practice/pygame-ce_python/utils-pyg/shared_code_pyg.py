import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def asset_path(relative_path):
    return os.path.join(BASE_PATH, relative_path)
