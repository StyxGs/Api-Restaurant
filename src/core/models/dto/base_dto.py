from dataclasses import dataclass


@dataclass
class BaseDTO:
    title: str
    description: str

    @property
    def get_data(self):
        return dict(title=self.title, description=self.description)
