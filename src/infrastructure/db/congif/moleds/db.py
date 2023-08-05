from dataclasses import dataclass


@dataclass
class DBConfig:
    user: str
    password: str
    host: str
    port: str
    name: str

    @property
    def make_url(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


@dataclass
class RedisConfig:
    host: str
    port: int
