class ArenaMoveService:
    def __init__(self, arena, players, port):
        self.arena = arena
        self.players = players
        self.port = port

    def set_coord(self, player, x, y):
        def clip(value, upper, lower=0):
            if value >= upper:
                return upper
            if value <= lower:
                return lower
            return value

        player.x = clip(x, self.arena.width)
        player.y = clip(y, self.arena.height)
        self.port.dump(self.arena, self.players)

    def player_move(self, player, direction):
        if direction == 0:
            if player.x <= self.arena.width - player.velocity:
                player.move(0)

        if direction == 1:
            if player.x >= player.velocity:
                player.move(1)

        if direction == 2:
            if player.y >= player.velocity:
                player.move(2)

        if direction == 3:
            if player.y <= self.arena.height - player.velocity:
                player.move(3)
        self.port.dump(self.arena, self.players)
