#!/usr/bin/env python2
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
# - Seeing issues with Python 3.12.1
# Unicode Dentist, Is it safe? http://www.imdb.com/title/tt0074860/quotes
# Copyright (C) 2011  Chris Clark
#
# Determine if file content is "safe", e.g. is it pure ASCII?
# Can specifiy an encoding check but it always looks for non-ASCII bytes.
# Encoding is used for display BUT it only really works for Single Byte encodings.
#

import glob
import os
import sys

def main(argv=None):
    if argv is None:
        argv = sys.argv

    '''Usage:
        encoding filename(s)_to_check
    '''
    # nasty argv command line argument parsing
    expect_encoding = 'us-ascii'
    filename_pattern = '*'

    guess_encoding = 'cp1252'
    guess_encoding = 'utf-8'

    if len(argv) > 1:
        # Assume filename and optional encoding
        # no need for web server mode (file mode it more reliable, we have the raw bytes)
        expect_encoding = argv[1]

        try:
            filename_pattern = argv[2]
        except IndexError:
            filename_pattern = '*'

    nl_bytes = '\n'.encode(expect_encoding)
    ll_bytes = '\r'.encode(expect_encoding)

    for filename in glob.glob(filename_pattern):
        print('%s:' % filename)
        f = open(filename, 'rb')
        entire_file_bytes = f.read()
        f.close()
        problem_lines = 0
        for line_count, line_bytes in enumerate(entire_file_bytes.split(nl_bytes), 1):
            #print(line_count)
            try:
                line_bytes.encode(expect_encoding)
            except UnicodeDecodeError:
                print('%d:%r' % (line_count, line_bytes))
                problem_lines += 1
        print('%d problem lines in %s' % (problem_lines, filename))

    return 0


if __name__ == "__main__":
    sys.exit(main())

