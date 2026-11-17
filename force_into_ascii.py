#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""See asciinator.py and force_into_utf8.py
"Force" (where possible) into 7-bit us-ascii, this will allow some non-ascii cahracters to be emitted - USE_ELINKS will catch more characters
"""

import codecs
import os
import sys

import asciinator
import force_into_utf8
from force_into_utf8 import treat_as_cp1252_handler


is_py3 = sys.version_info >= (3,)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    filename = argv[1]  # consider defaulting to stdin '-'

    try:
        out_filename = argv[2]
        if out_filename == '-u':
            out_filename = filename
    except IndexError:
        out_filename = None

    if filename == '-':
        if is_py3:
            f = sys.stdin.buffer
        else:
            f = sys.stdin
    else:
        f = open(filename, 'rb')
    data = f.read()
    f.close()

    # NOTE force_into_utf8.match_git_output side effect
    codecs.register_error('treat_as_cp1252', treat_as_cp1252_handler)
    data_unicode = data.decode('utf-8', errors='treat_as_cp1252')

    hacked_data = data_unicode.replace('\r', '')  # strip windows newlines

    # print('*' * 65)
    hacked_data = asciinator.my_simple_asciinator(hacked_data)  # NB returns Unicode string type, may not really be ASCII

    if out_filename:
        hacked_data = hacked_data.encode('us-ascii')  # moment of truth sanity check time
        f = open(out_filename, 'wb')  # May not be be 100% clean ascii now, assume default encoding ()almost certainly utf-8) is fine (which will also allow unmapped non-ascii characters to write to disk)
        f.write(hacked_data)
        f.close()
    else:
        # no filename
        print('** output filename NOT specified **')
        print(hacked_data)
        print('** output filename NOT specified **')

    return 0


if __name__ == '__main__':
    sys.exit(main())
