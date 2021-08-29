import os
from dotenv import dotenv_values
import CloudFlare


def _load():
    """
    Loads the config.
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


def _init_cf():
    return CloudFlare.CloudFlare(token=CFG.get('CF_API_KEY'))


CF = _init_cf()

def get_cf():
    return CF

