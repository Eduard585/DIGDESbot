city1 = u'\U0001F303'
city2 = u'\U0001F306'
city3 = u'\U0001F307'
bridges = u'\U0001F309'

map = {
    '🌃':city1,
    '06':city2,
    '07':city3,
    '09':bridges
}


def convert(surrogate):
    print(surrogate)
    return map[surrogate]

