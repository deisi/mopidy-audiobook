from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext
from mopidy.local import Library
from mopidy.local.json import JsonLibrary


__version__ = '0.1.0'

# TODO: If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-Audiobook'
    ext_name = 'audiobook'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['library'] = config.String()
        schema['media_dir'] = config.Path()
        schema['scan_timeout'] = config.Integer(
            minimum=1000, maximum=1000 * 60 * 60)
        schema['scan_flush_threshold'] = config.Integer(minimum=0)
        schema['scan_follow_symlinks'] = config.Boolean()
        schema['excluded_file_extensions'] = config.List(optional=True)
        return schema

    def setup(self, registry):
        
        from .frontend import AudiobookFrontend
        registry.add('frontend', AudiobookFrontend)

        from .backend import AudiobookBackend

        AudiobookBackend.libraries = registry['local:audiobook']
        
        registry.add('backend', AudiobookBackend)
        registry.add('local:audiobook', AudiobookLibrary)
        

class AudiobookLibrary(Library):
    
    ROOT_DIRECTORY_URI = 'audiobook:directory'
    name='audiobook'

    def __init__(self, config):
        logger.debug('AudiobookLibrary Init')
        self._config = config
        self._media_dir = config['audiobook']['media_dir']
    
