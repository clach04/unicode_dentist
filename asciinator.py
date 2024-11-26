#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""MS Word (and other similar tools that use the same editor control, Outlook, Excel etc.
replace standard 7-bit US-ASCII characters with "pretty" characters that are not portable.

Find them and destroy them!

Sample Usage:

    python asciinator.py FILENAME
    python asciinator.py FILENAME cp1252
    python asciinator.py FILENAME cp1252  > FILENAME_ascii

Ideas:
  * generate mappings for different encodings then apply to binary files (not Unicode strings), e.g. fix mixed encodings files (do utf-8, then cp1252, etc.)
  * Force utf-8 tool, do above and for any bytes above 127 (decimal) decode each (non-utf8 char) as cp1252 (failing that latin1) and force to utf-8 version
      * bascically a "smart" (or dumb..) replacement function - backslashreplace
            my_bytes = b'utf8 \xc2\xa9 win1252 \xa9'
            print(my_bytes.decode('utf-8', errors='backslashreplace'))
            See force_into_utf8.py
"""

import os
import sys

#import pdb ; pdb.set_trace()
# http://jwilk.net/software/python-elinks
try:
    if not os.environ.get('USE_ELINKS'):
        raise ImportError
    """Reasons to NOT use elinks
    cp1252 / win152 - 0xA0 - nbsp - non-breaking space - becomes "*" start in elinks
    c-cidilla ends up as two characters
    GBP currency symbol becomes becomes -L-
    """
    import elinks  # https://github.com/jwilk-archive/python-elinks
except ImportError:
    elinks = None



# I prefer the mappings in here compared with elinks.
# defaults to html
global_mappings_dict = {
    u'“': u'"',  # 201C  LEFT DOUBLE QUOTATION MARK
    u'”': u'"',  # 201D  RIGHT DOUBLE QUOTATION MARK
    u"‘": u"'",  # 2018  LEFT SINGLE QUOTATION MARK
    u"’": u"'",  # 2019  RIGHT SINGLE QUOTATION MARK
    u'–': u'-',  # 2013  EN DASH
    u'—': u'-',  # 2014  EM DASH
    #u'©': u'&copy;',  # 00A9  COPYRIGHT SIGN
    #u'©': u'(c)',  #  00A9  COPYRIGHT SIGN
    #u'®': u'&reg;',  # 00AE  REGISTERED SIGN
    #u'®': u'(R)',  # 00AE  REGISTERED SIGN
    #u'\xa0': u'&nbsp;',  # 'NO-BREAK SPACE' (U+00A0)
    #u'\xa0': u' ',  # 'NO-BREAK SPACE' (U+00A0)
    u'\xa3': u'GBP',  # Unicode Character British Currency Pound Sign (U+00A3)
    u'\xd7': u'x',  # Unicode Character Multiplication Sign (U+00D7)
    u'\xad': u'-',  # 'soft hyphen' (U+00AD) -- &shy;
    u'·': u'-',  # cp1252 0xb7 U+00B7 MIDDLE DOT
}

if os.environ.get('USE_HTML'):
    global_mappings_dict[u'©'] = u'&copy;'  #  00A9  COPYRIGHT SIGN
    global_mappings_dict[u'®'] = u'&reg;'  # 00AE  REGISTERED SIGN
    global_mappings_dict[u'™'] = u'&trade;'  # TRADE MARK SIGN (U+2122)
    global_mappings_dict[u'\xa0'] = u'&nbsp;'  # 'NO-BREAK SPACE' (U+00A0)
    global_mappings_dict[u'\u202F'] = u'&nbsp;'  # Narrow No-Break Space (NNBSP) (U+202F)
    #global_mappings_dict[] = 
elif os.environ.get('NO_HTML', True):
    global_mappings_dict[u'©'] = u'(c)'  #  00A9  COPYRIGHT SIGN
    global_mappings_dict[u'®'] = u'(R)'  # 00AE  REGISTERED SIGN
    global_mappings_dict[u'™'] = u'(TM)'  # TRADE MARK SIGN (U+2122)
    global_mappings_dict[u'\xa0'] = u' '  # 'NO-BREAK SPACE' (U+00A0)
    global_mappings_dict[u'\u202F'] = u' '  # Narrow No-Break Space (NNBSP) (U+202F)
    #global_mappings_dict[] = 


def my_simple_asciinator(in_str, mappings_dict=None):
    """Simple replacement of limited number of characters.

    @param in_str should already be a Unicode string type (NOTE this is NOT asserted/checked/enforced)
    """
    mappings_dict = mappings_dict or global_mappings_dict

    if elinks:
        result = in_str.encode('us-ascii', 'elinks')  # NOTE requires elinks import above to succeed
        result = result.decode('us-ascii')  # back to string
        return result

    result = in_str
    for char_to_replace in mappings_dict:
        #if char_to_replace == u'\202F':
        #    import pdb; pdb.set_trace()
        result = result.replace(char_to_replace, mappings_dict[char_to_replace])
    return result


def read_file(filename, encoding='utf-8', out_filename=None):
    """Dump to stdout or write to out_filename, assuming successfull conversion into 7-bit us-ascii
    """
    encoding = encoding or 'utf-8'
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    data = data.decode(encoding)

    data = data.replace('\r', '')  # strip windows newlines

    #print('*' * 65)
    data = my_simple_asciinator(data)  # NB returns Unicode string type, may not really be ASCII
    #data = data.encode('ASCII')
    #print(data,)
    r"""
    f = open(r'c:\tmp\d.txt', 'wb')
    f.write(data)
    f.close()
    """
    if out_filename:
        #import pdb; pdb.set_trace()
        data = data.encode('us-ascii')
        f = open(out_filename, 'wb')
        f.write(data)
        f.close()
    else:
        sys.stdout.write(data)
    #print('*' * 65)


def doit():
    test_data = u"""

# different endash, emdash, hypens

–
—

# different quotes

“66 and 99 quotes”

‘6 and 9 quotes’

# Symbols


TODO:

  * © copyright
  * ® registered trademark
  * pi?

"""
    print('*' * 65)
    print(my_simple_asciinator(test_data))  # NB returns Unicode string type, may not really be ASCII
    print('*' * 65)

    try:
        print(test_data.encode('ASCII', 'elinks'))  # NOTE requires elinks import above to succeed
    except LookupError:
        print('elinks needed for this demo/test')
    #print('*' * 65)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        filename = argv[1]
    except IndexError:
        filename = None

    try:
        encoding = argv[2]
    except IndexError:
        encoding = None  # will default to utf-8

    try:
        out_filename = argv[3]  # due to way read_file() reads entire file, this can be the same filename as input
        if out_filename == '-u':
            # use input filename as output
            out_filename = filename
    except IndexError:
        out_filename = None  # write to stdout

    if filename:
        read_file(filename, encoding=encoding, out_filename=out_filename)
    else:
        doit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
