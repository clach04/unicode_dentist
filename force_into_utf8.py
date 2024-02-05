#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""
"""

import codecs
import os
import sys


def treat_as_cp1252_handler(e):
    """Very specific handle to attempt to handle ONLY cp1252 in utf-8 moji-bake type scenario. Python 3.x ONLY
        encoding: the encoding currently being used.
        object: the string being encoded, or the bytes being decoded.
        start: the first index where we encounter an error.
        end: the last index where we encounter an error.
        reason: the error message.

    """
    if e is UnicodeEncodeError:
        raise NotImplementedError('UnicodeEncodeError')
    else: # e is UnicodeDecodeError
        """
        print('start %r' % e.start)
        print('end %r' % e.end)
        print('reason %r' % e.reason)
        print('object %r' % e.object)
        #print(' %r' % e.)
        """
        problem_bytes = e.object[e.start:e.end]
        #print('problem bytes %r' % problem_bytes)
        replacement_character = problem_bytes.decode('cp1252', errors='backslashreplace')  # this fails under Python 2.7 with same UnicodeDecodeError in callback error :-(
        """
        try:
            replacement_character = problem_bytes.decode('cp1252')
        except UnicodeDecodeError:
            # UnicodeDecodeError not supported in Python 2.7 in a callback :-(
            replacement_character = '\\x%s' % problem_bytes.hex()
        """
        #print('problem bytes treated as cp1252 (\\x means unmapped)%r' % replacement_character)
        return replacement_character, e.end
        #raise NotImplementedError('UnicodeDecodeError')


def doit():
    test_bytes = b'utf8 \xc2\xa9 win1252 \xa9'
    test_bytes = b'utf8 \xc2\xa9 win1252 \xa9 - 0x81 missing from cp1252 \x81'
    print('%r' % test_bytes)
    print('*' * 65)
    #print(test_bytes.decode('utf-8'))
    #print('*' * 65)
    print(test_bytes.decode('utf-8', errors='backslashreplace'))

    codecs.register_error('treat_as_cp1252', treat_as_cp1252_handler)
    print('*' * 65)
    print(test_bytes.decode('utf-8', errors='treat_as_cp1252'))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        filename = argv[1]
    except IndexError:
        filename = None

    try:
        out_filename = argv[2]
    except IndexError:
        out_filename = None

    if filename:
        f = open(filename, 'rb')
        data = f.read()
        f.close()

        codecs.register_error('treat_as_cp1252', treat_as_cp1252_handler)
        data_unicode = data.decode('utf-8', errors='treat_as_cp1252')
        hacked_data = data_unicode.encode('utf-8')

        f = open(out_filename, 'wb')
        f.write(hacked_data)
        f.close()
    else:
        doit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
