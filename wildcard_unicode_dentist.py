#!/usr/bin/env python2
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
# - Seeing display issues with Python 3.12.1, but it does run and return useful information
# Wildcard Unicode Dentist, Is it safe? http://www.imdb.com/title/tt0074860/quotes
# Needs Unicode Dentist
# Copyright (C) 2013 Chris Clark
#
# Determine if file content is "safe", e.g. is it pure ASCII?
# Can specifiy an encoding check but it always looks for non-ASCII bytes.
# Encoding is used for display BUT it only really works for Single Byte encodings.
#

import os
import sys
import glob

import unicode_dentist


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version.replace('\n', ' '), sys.platform.replace('\n', ' ')))
    # nasty argv command line argument parsing
    expect_encoding = 'us-ascii'
    print('using: %r' % expect_encoding)

    print(repr(argv))
    print(len(argv))
    if len(argv) > 1:
        # Assume filename and optional encoding
        # no need for web server mode (file mode it more reliable, we have the raw bytes)
        expect_encoding = argv[1]

    try:
        filename_pattern_list = argv[2:]
    except IndexError:
        pass

    if not filename_pattern_list:
        filename_pattern_list = ['*']

    print('filename_pattern_list: %r' % filename_pattern_list)
    for filename_pattern in filename_pattern_list:
        for filename in glob.glob(filename_pattern):
            print('about to check: %r' % filename)
            params = ['unicode_dentist', filename, expect_encoding]
            unicode_dentist.main(params)

    return 0


if __name__ == "__main__":
    sys.exit(main())


