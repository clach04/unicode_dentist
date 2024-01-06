# Unicode Dentist

# -*- coding: cp-1252 -*-

Is it safe!?
[Marathon Man - do not click on this if you are squeamish!](https://www.youtube.com/watch?v=avNraWT8CSI)

  * Is this file US-ASCII (7 bit) safe?
  * Is this file UTF-8 safe?
  * Is this file cp1252 safe?
  * Is this file ... safe?


## Tools

Python 3.x and 2.7 (maybe 2.x?) tools:

  * unicode_dentist.py - find invalid **bytes** in a single file, will report statistics and context
  * wildcard_unicode_dentist.py - same as above but handles multiple files in a list (potentially with wild cards, even under Microsoft Windows)
  * line_check.py - display lines that are not in the expected encoding, along with line number and final "bad" line number count

## Examples

Run on this readme.

### line_check example

    $ ./line_check.py us-ascii README.md
    README.md:
    28:'Euro symbol: \x80'
    29:'Copyright symbol: \xa9'
    30:'Euro symbol (again): \x80'
    48:'    README.md:10: 128 \x80 @ 152'
    50:'    Euro symbol: \x80'
    52:'    README.md:11: 169 \xa9 @ 171'
    54:'    Copyright symbol: \xa9'
    56:'    README.md:12: 128 \x80 @ 193'
    58:'    Euro symbol (again): \x80'
    61:'    169 0xa9 not valid us-ascii character \xa9 occurrences 1'
    62:'    128 0x80 not valid us-ascii character \x80 occurrences 2'
    11 problem lines in README.md


### unicode_dentist example

Example usage:

    python unicode_dentist.py unicode_dentist.py
    python unicode_dentist.py README.md

Euro symbol: €
Copyright symbol: ©
Euro symbol (again): €

Sample output pure US-ASCII file:

    C:\tmp>unicode_dentist.py unicode_dentist.py
    ['C:\\tmp\\unicode_dentist.py', 'unicode_dentist.py']
    2
    expected_encoding: us-ascii
    'unicode_dentist.py' is valid us-ascii

Sample output non ASCII:

    C:\>unicode_dentist.py README.md
    ['C:\\unicode_dentist.py', 'README.md']
    2
    expected_encoding: us-ascii
    us-ascii '\xa9'
    us-ascii '\x80'
    README.md:10: 128 € @ 152
    'Euro symbol: \x80'
    Euro symbol: €

    README.md:11: 169 © @ 171
    'Copyright symbol: \xa9'
    Copyright symbol: ©

    README.md:12: 128 € @ 193
    'Euro symbol (again): \x80'
    Euro symbol (again): €

    ========= character table =========
    169 0xa9 not valid us-ascii character © occurrences 1
    128 0x80 not valid us-ascii character € occurrences 2
    =================================================================

