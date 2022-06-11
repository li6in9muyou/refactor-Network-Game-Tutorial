import socket

import pygame


class PyGameRenderPort:
    def __init__(self, arena, players, w=500, h=500, name='PyGameRenderPort'):
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)
        self.dump(arena, players)

    def dump(self, arena, players):
        self.screen.fill(arena.ground_color)
        for player in players:
            pygame.draw.rect(self.screen, player.color, (player.x, player.y, 50, 50), 0)
            pygame.display.update()


class OnlinePortAndAdapter:
    @staticmethod
    def parse_data(remote_data):
        try:
            d = remote_data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except IndexError:
            return 0, 0

    def __init__(self, arena_service, players, host='localhost', port=5555):
        self.arena_service = arena_service
        self.local_player, self.remote_player = players
        self.prev_remote_x = -1
        self.prev_remote_y = -1

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (host, port)
        self.client.connect(self.addr)
        self.local_player_id = self.client.recv(2048).decode()

    def dump(self, *_):
        pass

    def on_init(self):
        data = f"{str(self.local_player_id)}:"
        self.client.send(str.encode(data))
        self.arena_service.set_coord(self.local_player, *self.parse_data(self.client.recv(2048).decode()))

    def on_update(self):
        data = f"{str(self.local_player_id)}:{str(self.local_player.x)},{str(self.local_player.y)}"
        self.client.send(str.encode(data))
        now_remote_x, now_remote_y = self.parse_data(self.client.recv(2048).decode())

        if self.prev_remote_x != now_remote_x or self.prev_remote_y != now_remote_y:
            self.prev_remote_x = now_remote_x
            self.prev_remote_y = now_remote_y
            self.arena_service.set_coord(
                self.remote_player,
                self.prev_remote_x, self.prev_remote_y
            )


class CombinedPort:
    def __init__(self):
        self.ports = []

    def add_port(self, port):
        self.ports.append(port)

    def dump(self, arena, players):
        for port in self.ports:
            port.dump(arena, players)
