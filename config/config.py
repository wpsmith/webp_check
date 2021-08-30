import os
from dotenv import dotenv_values


def _load():
    """
    Loads the config.py.
    :rtype: Dict[str, Optional[str]]
    """
    cfg = {
        **dotenv_values(".env.default"),
        **dotenv_values(".env"),
        **os.environ,  # override loaded values with environment variables
    }

    return cfg


CFG = _load()


def get():
    return CFG

