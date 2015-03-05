#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
A script to delete songs from your Google Music library using https://github.com/simon-weber/Unofficial-Google-Music-API.
More information at https://github.com/thebigmunch/gmusicapi-scripts.

Usage:
  gmdelete.py (-h | --help)
  gmdelete.py [options] [-f FILTER]... [-F FILTER]...

Options:
  -h, --help                            Display help message.
  -u USERNAME, --user USERNAME          Your Google username or e-mail address.
  -p PASSWORD, --pass PASSWORD          Your Google or app-specific password.
  -l, --log                             Enable gmusicapi logging.
  -d, --dry-run                         Output list of songs that would be deleted.
  -q, --quiet                           Don't output status messages.
                                        With -l,--log will display gmusicapi warnings.
                                        With -d,--dry-run will display song list.
  -f FILTER, --include-filter FILTER    Include Google songs by field:pattern filter (e.g. "artist:Muse").
                                        Songs can match any filter criteria.
                                        This option can be set multiple times.
  -F FILTER, --exclude-filter FILTER    Exclude Google songs by field:pattern filter (e.g. "artist:Muse").
                                        Songs can match any filter criteria.
                                        This option can be set multiple times.
  -a, --include-all                     Songs must match all include filter criteria to be included.
  -A, --exclude-all                     Songs must match all exclude filter criteria to be excluded.
  -y, --yes                             Delete songs without asking for confirmation.

Patterns can be any valid Python regex patterns.
"""

from __future__ import unicode_literals

import logging

from docopt import docopt

from gmusicapi_wrapper import MobileClientWrapper

QUIET = 25
logging.addLevelName(25, "QUIET")

logger = logging.getLogger('gmusicapi_wrapper')
sh = logging.StreamHandler()
logger.addHandler(sh)


def main():
	cli = dict((key.lstrip("-<").rstrip(">"), value) for key, value in docopt(__doc__).items())

	if cli['quiet']:
		logger.setLevel(QUIET)
	else:
		logger.setLevel(logging.INFO)

	mcw = MobileClientWrapper()
	mcw.login(cli['user'], cli['pass'])

	include_filters = [tuple(filt.split(':', 1)) for filt in cli['include-filter']]
	exclude_filters = [tuple(filt.split(':', 1)) for filt in cli['exclude-filter']]

	songs_to_delete, _ = mcw.get_google_songs(include_filters, exclude_filters, cli['include-all'], cli['exclude-all'])

	if cli['dry-run']:
		logger.info("Found {0} songs to delete".format(len(songs_to_delete)))

		if songs_to_delete:
			logger.info("\nSongs to delete:\n")

			for song in songs_to_delete:
				title = song.get('title', "<empty>")
				artist = song.get('artist', "<empty>")
				album = song.get('album', "<empty>")
				song_id = song['id']

				logger.log(QUIET, "{0} -- {1} -- {2} ({3})".format(title, artist, album, song_id))
		else:
			logger.info("\nNo songs to delete")
	else:
		if songs_to_delete:
			confirm = cli['yes'] or cli['quiet']
			logger.info("")

			if confirm or raw_input("Are you sure you want to delete {0} song(s) from Google Music? (y/n) ".format(len(songs_to_delete))) in ("y", "Y"):
				logger.info("\nDeleting {0} songs from Google Music\n".format(len(songs_to_delete)))

				songnum = 0
				total = len(songs_to_delete)
				pad = len(str(total))

				for song in songs_to_delete:
					mcw.api.delete_songs(song['id'])
					songnum += 1

					title = song.get('title', "<empty>")
					artist = song.get('artist', "<empty>")
					album = song.get('album', "<empty>")
					song_id = song['id']

					logger.debug("Deleting {0} -- {1} -- {2} ({3})".format(title, artist, album, song_id))
					logger.info("Deleted {num:>{pad}}/{total} song(s) from Google Music".format(num=songnum, pad=pad, total=total))
			else:
				logger.info("\nNo songs deleted.")
		else:
			logger.info("\nNo songs to delete")

	mcw.logout()
	logger.info("\nAll done!")


if __name__ == '__main__':
	main()