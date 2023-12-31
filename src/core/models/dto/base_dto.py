from dataclasses import dataclass


@dataclass
class BaseDTO:
    title: str | None = None
    description: str | None = None

    @property
    def get_data_without_none(self) -> dict:
        dto = dict(title=self.title, description=self.description)
        return {name: data for name, data in dto.items() if data}
