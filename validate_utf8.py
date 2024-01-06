#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""GitJournal silently hides non-utf-8 files.
Super confusing when/if this happens.

Sanity check all (file pattern files).

Poor mans https://github.com/clach04/unicode_dentist

Ideas:
 * flag to append the text "invalid utf8 in this file" to end of files
     * assuming not already at EOF
"""

import glob
import os
import sys

is_win = sys.platform.startswith('win')
extensions_to_check = ['.md', '.txt']

def walker(directory_name, process_file_function=None, process_dir_function=None, extra_params_dict=None):
    """extra_params_dict optional dict to be passed into process_file_function() and process_dir_function()

    def process_file_function(full_path, extra_params_dict=None)
        extra_params_dict = extra_params_dict or {}
    """
    extra_params_dict or {}
    # TODO scandir instead... would be faster - but for py2.7 requires external lib
    for root, subdirs, files in os.walk(directory_name):
        if process_file_function:
            for filepath in files:
                full_path = os.path.join(root,filepath)
                process_file_function(full_path, extra_params_dict=extra_params_dict)
        if process_dir_function:
            for sub in subdirs:
                full_path = os.path.join(root, sub)
                process_dir_function(full_path, extra_params_dict=extra_params_dict)

def per_file_function_callback(full_path, extra_params_dict=None):
    # NOTE does directory ignoring here, would be more efficient in walker()

    #print('full_path %r' % full_path)
    # potentiall ignore git (TODO hg, svn, ...) irrespective of `ignore_directory_list`
    #git_dir = os.sep + '.git' + os.sep  # just to be sure?
    # Take a look at https://geoff.greer.fm/2016/09/26/ignore/ .ignore file
    ignore_directory_list = extra_params_dict.get('ignore_directory_list', [])  # list of full directory name (not an extract)
    for x in ignore_directory_list:
        tmp_name  = os.sep + x + os.sep  # only match whole directory path rather than a fragment
        if tmp_name in full_path:
            return

    #if 'Games2' in full_path:
    #    import pdb  ; pdb.set_trace()

    check_this_one = False
    for extension in extensions_to_check:
        if full_path.endswith(extension):
            check_this_one = True
            break

    if check_this_one:
        #print(full_path)
        check_file(full_path)
        extra_params_dict['counter'] += 1

stop_on_invalid_encoding = True
if os.environ.get('DO_NOT_STOP'):
    stop_on_invalid_encoding = False
file_encoding = os.environ.get('FILE_ENCODING', 'utf-8')
global_bad_file_counter = 0
def check_file(filename):
        f = open(filename, 'rb')
        d = f.read()
        f.close()
        #offset = 2424
        #print('%r' % d[offset - 10:offset + 10])
        #import pdb; pdb.set_trace()
        try:
            s = d.decode(file_encoding)
        except UnicodeDecodeError:
            global global_bad_file_counter
            global_bad_file_counter += 1
            print('%s is not %s' % (filename, file_encoding))
            print('Consider using force_into_utf8.py or manually fix')
            if stop_on_invalid_encoding:
                raise  # re-raise for now, potential to skip and carry on processing with warning only


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version.replace('\n', ' '), sys.platform.replace('\n', ' ')))

    """Usage:
    No Parameters

        validate_utf8.py

    When called with no parameters will **recursively** search current path for *.md and *.txt files (see `extensions_to_check`) and check if they are valid utf-8.
      * Some directories will be ignored (for example .git), see `ignore_directory_list` for more details.
      * File scan will STOP on first "bad" file, unless operating system variable `DO_NOT_STOP` is set (to anything).
      * File encodigng to check can be specified via operating system environment variable `FILE_ENCODING`, example:
    examples:

        env FILE_ENCODING=us-ascii ./validate_utf8.py
        env FILE_ENCODING=us-ascii DO_NOT_STOP=true ./validate_utf8.py

        export FILE_ENCODING=us-ascii
        py -3 validate_utf8.py

        set FILE_ENCODING=us-ascii
        py -3 validate_utf8.py

    With Parameters
        validate_utf8.py pattern1 [pattern2]

    When called with params will use those as wild cards searches and then check ONLY those. Can also use non-wild card arguments.
    Example:

        validate_utf8.py *.md *.txt
    NOTE this is NOT recursive (see no parameter mode)
    """
    if is_win:
        filenames = []
        for filename_pattern in argv[1:]:
            filenames += glob.glob(filename_pattern)
    else:
        filenames = argv[1:]

    #doit()
    # ./validate_utf8.py  *.md *.txt
    # py -3 validate_utf8.py  *.md *.txt
    print('%d files to check explictly' % len(filenames))
    #print(filenames)
    if filenames:
        for filename_counter, filename in enumerate(filenames):
            # TODO progress log
            check_file(filename)
    else:
        print('recursively checking')
        #print('ERROR No files to check')
        #raise NotImplementedError('ERROR No files to check')
        extra_params_dict = {
            'counter': 0,
            'ignore_directory_list': ['.git', '.hg', '__pycache__', '.mozilla', '.cache'],  # ignore directory list, TODO consider .ignore file support
        }

        dir_name = '.'
        print('checking %s recursively' % dir_name)
        walker(dir_name, process_file_function=per_file_function_callback, extra_params_dict=extra_params_dict)
        filename_counter = extra_params_dict['counter']
        #print('checked %d files' % extra_params_dict['counter'])
        print('checked %d files' % filename_counter)


    if not stop_on_invalid_encoding and global_bad_file_counter:
        print('BAD %d files' % global_bad_file_counter)

    return 0


if __name__ == "__main__":
    sys.exit(main())
