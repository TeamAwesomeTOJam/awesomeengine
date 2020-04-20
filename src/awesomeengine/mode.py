from abc import ABC, abstractmethod


class Mode(ABC):

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def leave(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self):
        pass
