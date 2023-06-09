"""
Buttons's image asset is "0.png" in "assets/interface/button/{button._id}".
"""
import os, pygame
from typing import Callable
from sevenlives.utils import ScrW, ScrH, getAssetFolder
from sevenlives.interface import Mouse
from sevenlives.interface.status import UIStatus

class Button:
    def __init__(self,
        id: str,
        pos: pygame.Vector2,
        callback: Callable[[], None] = lambda: None,

        size: tuple[int, int] = (200, 50),
        color: pygame.Color = pygame.Color(51, 51, 51),
        text: str = None,
        textColor: pygame.Color = pygame.Color(235, 235, 235)
    ):
        self._id = id
        self._status: UIStatus = UIStatus.IDLE
        self._callback = callback

        # Surface
        self._statusImages = {}
        for status in UIStatus.getValues():
            if os.path.exists(self.getStatusPath(status)):
                self._statusImages[status.getId()] = pygame.image.load(self.getStatusPath(status)).convert_alpha()

                if status == UIStatus.IDLE:
                    size = self._statusImages["idle"].get_rect().size

        self._rect = pygame.Rect(pos.x, pos.y, size[0], size[1])
        self._surface = pygame.Surface(self._rect.size).convert_alpha()
        self._surface.fill(pygame.Color(0, 0, 0, 0))

        if "idle" not in self._statusImages.keys():
            self._statusImages = {}

            self._surface.fill(color)
            font = pygame.font.SysFont("Arial", int(self._rect.h/2))
            textSurf = font.render(text if text != None else self._id.capitalize(), False, textColor)
            self._surface.blit(textSurf, textSurf.get_rect(center=self._surface.get_rect().center))

        # Sound
        self._clickSound = pygame.mixer.Sound(getAssetFolder("interface", "button", "click.wav"))

    def getStatus(self) -> UIStatus:
        return self._status
    def getStatusPath(self, forceStatus: UIStatus = None) -> str:
        return getAssetFolder("interface", "button", self._id,
            f"{forceStatus.getId() if forceStatus != None else self.getStatus().getId()}.png"
        )

    def update(self):
        self._surface.set_alpha(255)
        rect = pygame.Rect(ScrW()*self._rect.x/640, ScrH()*self._rect.y/360, ScrW()*self._rect.w/360, ScrH()*self._rect.h/360)

        if rect.collidepoint(*Mouse.getPos()):
            self._surface.set_alpha(127)

            if Mouse.isReleased() and rect.collidepoint(*Mouse.getPressedPos()):
                self._callback()
                self._clickSound.play()

            self._status = UIStatus.CLICKED if Mouse.isPressed() else UIStatus.IDLE
            if Mouse.isPressed(): self._surface.set_alpha(255)
        else:
            self._status = UIStatus.IDLE

    def draw(self, surface: pygame.Surface):
        surf = self._surface.copy()
        for statusID, img in self._statusImages.items():
            if statusID == self._status.getId():
                surf.fill(pygame.Color(0, 0, 0, 0))
                surf.blit(img, img.get_rect(center=surf.get_rect().center))

        surface.blit(surf, self._rect)