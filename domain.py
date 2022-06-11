class Player:
    def __init__(self, init_x=-1, init_y=-1, color=(100, 100, 100)):
        self.color = color
        self.y = init_y
        self.x = init_x
        self.velocity = 2

    def move(self, direction):
        """
        :param direction: 0 - 3 (right, left, up, down)
        :return: None
        """

        if direction == 0:
            self.x += self.velocity
        elif direction == 1:
            self.x -= self.velocity
        elif direction == 2:
            self.y -= self.velocity
        elif direction == 3:
            self.y += self.velocity
        else:
            raise RuntimeError(f'Player: unknown move direction: {direction}')


class Arena:
    def __init__(self, width, height, players):
        self.players = players
        self.width = width
        self.height = height
        self.ground_color = (255, 255, 255)
