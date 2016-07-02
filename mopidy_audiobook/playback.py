from __future__ import unicode_literals

import logging
import os

from mopidy import backend
#from mopidy.local import translator


logger = logging.getLogger(__name__)


class AudiobookPlaybackProvider(backend.PlaybackProvider):

    def play():
        logger.warning('AudiobookPlaybackProvider.play called')
        return False

    def translate_uri(self, uri):
        logger.warning('AudiobookPlaybackProvider.translate_uri uri:%s', uri)
        #ret = translator.local_uri_to_file_uri(
        #    uri, self.backend.config['audiobook']['media_dir'])
        ret = uri
        return ret
