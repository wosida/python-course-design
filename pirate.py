def pirate_game_5(m):
    pirates = list(range(1, m + 1))
    index = 0
    while len(pirates) > m / 2:
        index = (index + 4) % len(pirates)
        pirates.pop(index)
    return pirates


def pirate_game_7(m):
    pirates = list(range(1, m + 1))
    index = 0
    while len(pirates) > m / 2:
        index = (index + 6) % len(pirates)
        pirates.pop(index)
    return pirates


def callback(result):
    print("留在船上的海盗最初排序的序号:", result)


def main():
    m = 40
    n = 7
    if n == 5:
        result = pirate_game_5(m)
    elif n == 7:
        result = pirate_game_7(m)
    callback(result)


if __name__ == "__main__":
    main()
