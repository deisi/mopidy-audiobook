from __future__ import unicode_literals

import logging

from mopidy import core

import pykka

import os
import json

from mopidy_audiobook import Extension

logger = logging.getLogger(__name__)

class AudiobookFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(AudiobookFrontend, self).__init__()
        self.core = core

        # dir to save database file to
        ext = Extension()
        self.data_dir = ext.get_data_dir(config)
        self.data_file = os.path.join(self.data_dir, 'database')
        self.db = self._get_db()

    def _get_db(self):
        # UGLY as hell
        db = {}
        if os.path.isfile(self.data_file):
            fd = open(self.data_file, 'r')
            try:
                db = json.loads(fd.read())
            except ValueError:
                logger.info('audiobook database currupted.'
                            'Creating new empty database')
                fd.close()
                return {}
            
            fd.close()
            if type(db) is not type({}):
                logger.info('audiobook database currupted.'
                            'Creating new empty database')
                db = {}
        return db

    def _write_db(self):
        """ writes position of current track to databse"""
        dump = json.dumps(self.db)
        fd = open(self.data_file, 'w')
        fd.write('%s' % dump)
        fd.close()

    def track_playback_paused(self, tl_track, time_position):
        # save position to audiobook database
        self.db['%s' % tl_track.track] = time_position
        self._write_db()

    def track_playback_started(self, tl_track):
        logger.info('frontened detected playback of %s', tl_track)
        time_position = self.db.get('%s' % tl_track.track, 0)
        self.core.playback.seek(time_position)
        self.core.playback.play(tl_track)

    def track_playback_ended(self, tl_track, time_position):
        # remove finished audiobook from database 
        self.db.pop('%s' % tl_track.track, None)
        self._write_db()
