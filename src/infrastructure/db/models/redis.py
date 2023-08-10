from abc import ABC, abstractmethod


class Base(ABC):

    @abstractmethod
    def get_keys(self):
        pass
