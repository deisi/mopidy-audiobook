from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.local import storage

import pykka

from . import library, playback

from mopidy_audiobook import Extension

logger = logging.getLogger(__name__)


class AudiobookBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = ['audiobook']
    libraries = []

    def __init__(self, config, audio):
        super(AudiobookBackend, self).__init__()

        self.config = config
        storage.check_dirs_and_files(config)

        libraries = dict((l.name, l) for l in self.libraries)
        library_name = config['audiobook']['library']

        if library_name in libraries:
            this_library = libraries[library_name](config)
            logger.debug('Using %s as the audiobook library', library_name)
        else:
            this_library = None
            logger.warning('Audiobook library %s not found', library_name)

        
        self.library = library.AudiobookLibraryProvider(backend=self,
                                                        library=this_library)
        self.playback = playback.AudiobookPlaybackProvider(audio=audio,
                                                           backend=self)
