from flask.cli import load_dotenv
from requests import post

load_dotenv()


def test_register_player():
    r = post("http://127.0.0.1:4000/register", json={
        "role": "gamer",
        "platform": "js"
    })
    r.raise_for_status()
    client_id = r.json()["client_id"]

    assert client_id == "127.0.0.1/gamer/js"
