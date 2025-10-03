from flask.cli import load_dotenv
from requests import post

load_dotenv()


def test_register_player():
    r = post("http://127.0.0.1:4000/register")
    r.raise_for_status()
    client_id = r.json()["client_id"]

    assert client_id == "MTI3LjAuMC4x"  # 127.0.0.1
