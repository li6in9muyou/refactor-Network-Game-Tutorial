import pygame

from adapter import KeyboardInputAdapter, TwoPlayerAdapter
from domain import Player, Arena
from port import CombinedPort, PyGameRenderPort, OnlinePortAndAdapter
from service import ArenaMoveService

if __name__ == '__main__':
    local = Player(color=(30, 200, 30))
    remote = Player(color=(200, 80, 80))
    players = [local, remote]
    arena = Arena(500, 500, players)

    port = CombinedPort()
    service = ArenaMoveService(arena, players, port)

    local_agent = KeyboardInputAdapter(service, local)
    remote_agent = OnlinePortAndAdapter(service, players)

    port.add_port(PyGameRenderPort(arena, players))
    port.add_port(remote_agent)

    adapter = TwoPlayerAdapter(local_agent, remote_agent)

    clock = pygame.time.Clock()
    run = True

    adapter.on_init()
    while run:
        clock.tick(90)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.K_ESCAPE:
                run = False

        adapter.on_update()

    pygame.quit()
