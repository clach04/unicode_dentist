#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""See asciinator.py
"""

import codecs
import os
import sys


is_py3 = sys.version_info >= (3,)

# if match_git_output  is False, attempt to treat as cp1252... which might fail
# if match_git_output  is True, emit "<ff>" (without double quotes) the same way git escapes non-ascii.
# if it turns out not to be valid cp1252 then this NEEDS to be True
# TODO add support so false means attemp cp1252, and then fall back if that fails
match_git_output = False
#match_git_output = True

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
        if match_git_output:
            # NOTE doesn't actually get here, exception handlers not supportted in 2.7
            hex_representation = ''.join(hex(single_byte) for single_byte in problem_bytes)  # quick and dirty gex multiple 0x...
            #replacement_character = hex_representation.replace('0x', '\\x')  # the way Python3 handles it above
            replacement_character = '<%s>' % hex_representation.replace('0x', '')  # the way git handles it
        else:
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
    print(test_bytes.decode('utf-8', errors='backslashreplace'))  # works only for py3

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

        if out_filename:
            f = open(out_filename, 'wb')
            f.write(hacked_data)
            f.close()
        else:
            # no filename
            print('** output filename NOT specified **')
            print(hacked_data)
            print('** output filename NOT specified **')
    else:
        print('** input filename NOT specified, running demo **')
        doit()
        print('** input filename NOT specified, running demo **')

    return 0


if __name__ == "__main__":
    sys.exit(main())
