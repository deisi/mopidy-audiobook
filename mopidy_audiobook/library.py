from __future__ import unicode_literals

import logging
#import os
#import sys
#import operator
#import urllib2

from mopidy import models
import mopidy_audiobook as audiobook
from mopidy.local.library import LocalLibraryProvider
#from mopidy.audio import scan, tags
#from mopidy.internal import path

logger = logging.getLogger(__name__)

class AudiobookLibraryProvider(LocalLibraryProvider):

    root_directory = models.Ref.directory(
        uri=audiobook.Library.ROOT_DIRECTORY_URI, name='Audiobooks')
