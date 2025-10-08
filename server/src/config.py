from dataclasses import dataclass
from os import environ


@dataclass
class Config:
    client_id: str

    @staticmethod
    def load():
        try:
            return Config(**{
                "client_id": environ.get("client_id", "server")
            })
        except KeyError as e:
            print(str(e.add_note("Did you set the environment variables?")))
            raise e
