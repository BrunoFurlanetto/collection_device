import json
import os
from .serial_client import SerialClient


# Singleton client instance
def _load_serial_client():
    cfg_path = os.path.join('src', 'config', 'session_config.json')
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"Session config not found at {cfg_path}")

    with open(cfg_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    port = cfg.get('port')
    if not port:
        raise KeyError("`port` not found in session_config.json")

    # Instantiate client
    client = SerialClient(port)
    return client


_serial_client = None


def get_client():
    global _serial_client
    if _serial_client is None:
        _serial_client = _load_serial_client()
    return _serial_client


def send_familiarization(sense: str, test_type: str) -> str:
    """
    Sends a familiarization command to the ESP32 and returns its response.
    """
    client = get_client()
    cmd = f"START_FAMILIARIZATION:{sense},{test_type}"
    return client.send_and_receive(cmd)


def send_test(sense: str, test_type: str) -> str:
    """
    Sends a start-test command to the ESP32 and returns its response.
    """
    client = get_client()
    cmd = f"START_TEST:{sense},{test_type}"
    print('Foi')
    resp = client.send_and_receive(cmd)
    print(resp)
    return resp


def close_client():
    """
    Closes the underlying serial connection.
    """
    global _serial_client
    if _serial_client:
        _serial_client.close()
        _serial_client = None
