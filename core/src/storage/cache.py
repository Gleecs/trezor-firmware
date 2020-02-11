from trezor.crypto import random

if False:
    from typing import Optional, Dict, List

_MAX_SESSIONS_COUNT = 8  # TODO

APP_COMMON_SEED = 0
APP_COMMON_SEED_WITHOUT_PASSPHRASE = 1
APP_CARDANO_ROOT = 2
APP_MONERO_LIVE_REFRESH = 3

_active_session_id = None  # type: Optional[bytes]
_caches = {}  # type: Dict[bytes, Dict[int, Any]]
_session_ids = []  # type: List[bytes]

if False:
    from typing import Any


def _move_session_ids_queue(session_id: bytes) -> None:
    # Move the LRU session ids queue.
    if session_id in _session_ids:
        _session_ids.remove(session_id)
    elif len(_session_ids) == _MAX_SESSIONS_COUNT:
        remove_session_id = _session_ids.pop()
        del _caches[remove_session_id]

    _session_ids.insert(0, session_id)


def get_active_session_id() -> Optional[bytes]:
    return _active_session_id


def start_session(received_session_id: bytes=None) -> bytes:
    if received_session_id and received_session_id in _session_ids:
        session_id = bytes(received_session_id)
    else:
        session_id = random.bytes(32)
        _caches[session_id] = {}

    global _active_session_id
    _active_session_id = session_id
    _move_session_ids_queue(session_id)
    return _active_session_id


def set(key: int, value: Any) -> None:
    if _active_session_id is None:
        return None  # no session active
    _caches[_active_session_id][key] = value


def get(key: int) -> Any:
    if _active_session_id is None:
        return None  # no session active
    return _caches[_active_session_id].get(key)


def clear() -> None:
    global _active_session_id
    global _caches
    global _session_ids

    _active_session_id = None
    _caches.clear()
    _session_ids.clear()
