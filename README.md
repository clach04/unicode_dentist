# Unicode Dentist

# -*- coding: cp-1252 -*-

Is it safe!?

Is this file US-ASCII (7 bit) safe?

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