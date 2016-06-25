from __future__ import unicode_literals

import logging

from mopidy import backend, models

logger = logging.getLogger(__name__)

def get_config_dir(config):
    try:
        return Extension.get_config_dir(config)
    except EnvironmentError as e:
        logger.warning('Cannot access %s config directory: %s',
                       Extension.dist_name, strerror(e))
    except Exception as e:
        logger.warning('Cannot access %s config directory: %s',
                       Extension.dist_name, e)
    return None


class AudiobookLibraryProvide(backend.LibraryProvider):
