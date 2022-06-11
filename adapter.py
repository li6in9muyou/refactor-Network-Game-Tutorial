import pygame


class KeyboardInputAdapter:
    def __init__(self, arena_service, player):
        self.arena_service = arena_service
        self.player = player

    def on_update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.arena_service.player_move(self.player, 0)
        if keys[pygame.K_LEFT]:
            self.arena_service.player_move(self.player, 1)
        if keys[pygame.K_UP]:
            self.arena_service.player_move(self.player, 2)
        if keys[pygame.K_DOWN]:
            self.arena_service.player_move(self.player, 3)

    def on_init(self):
        pass


class TwoPlayerAdapter:
    def __init__(self, a, b):
        self.adapter_a = a
        self.adapter_b = b

    def on_update(self):
        self.adapter_a.on_update()
        self.adapter_b.on_update()

    def on_init(self):
        self.adapter_a.on_init()
        self.adapter_b.on_init()
