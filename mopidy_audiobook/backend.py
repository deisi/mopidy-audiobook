from __future__ import unicode_literals

import logging

from mopidy import backend

import pykka

from . import library, playback

logger = logging.getLogger(__name__)


class AudiobookBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = ['audiobook']

    def __init__(self, config, audio):
        super(AudiobookBackend, self).__init__()
        self.library = library.AudiobookLibraryProvider(backend=self, config=config)
        self.playback = backend.AudiobookPlaybackProvider(audio=auido, backend=self)
        
