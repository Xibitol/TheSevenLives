import os, pygame
from sevenlives.utils import ScrW, ScrH
from sevenlives.level.base import Level
from sevenlives.interface import Button

class MainLevel:
    def __init__(self):
        self.__parent = Level("menu")
        self._buttons: list[Button] = [
            Button("start", pygame.Vector2(0, 0), self.startClicked),
            Button("continue", pygame.Vector2(0, 0), self.continueClicked),
            Button("quit", pygame.Vector2(0, 0), self.quitClicked),
        ]

        space = pygame.Vector2(0, 20)
        origin = pygame.Vector2(
            self._getInternalSurface().get_width()*2/3,
            self._getInternalSurface().get_height()/2 - self._buttons[0]._rect.h
        )

        # Logo
        self._logo = pygame.image.load(os.path.join(self.__parent.getPath(), "logo.png"))
        self._logoRect = self._logo.get_rect(
            bottomleft = origin - space - pygame.Vector2((self._logo.get_rect().w - self._buttons[0]._rect.w)/2, 0)
        )

        # Buttons
        for (i, button) in enumerate(self._buttons):
            button._rect.topleft = self._buttons[i - 1]._rect.bottomleft + space if i > 0 else origin

        # Credits
        self._cdtText = pygame.font.SysFont("Arial", 15).render(
            "The Seven Lives - A NSI project by Xibitol, Nagisou and Mélody - licensed under GNU GPL v3.",
            True,
            pygame.Color(235, 235, 235)
        )
        self._cdtRect = self._cdtText.get_rect(bottomleft = pygame.Vector2(
            10,
            self._getInternalSurface().get_height() - 10
        ))

    # GETTERS
    def _getInternalSurface(self) -> pygame.Surface:
        return self.__parent._getInternalSurface()

    # FUNCTIONS
    def update(self, deltatime):
        self.__parent.update(deltatime)

        for button in self._buttons:
            button.update()

    def _drawInternally(self, visibleRect: pygame.Rect):
        self.__parent._drawInternally(visibleRect)

        for button in self._buttons:
            button.draw(self._getInternalSurface())

        self._getInternalSurface().blit(self._logo, self._logoRect)
        self._getInternalSurface().blit(self._cdtText, self._cdtRect)
    def draw(self, surface: pygame.Surface):
        self._drawInternally(surface.get_rect(topleft=self.__parent._position))
        self.__parent.draw(surface, False)

    # BUTTONS FUNCTIONS
    def startClicked(self):
        pass
    def continueClicked(self):
        pass
    def quitClicked(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
