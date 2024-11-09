#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
# Unicode Dentist, Is it safe? http://www.imdb.com/title/tt0074860/quotes
# Copyright (C) 2011  Chris Clark
#
# Determine if file content is "safe", e.g. is it pure ASCII?
# Can specifiy an encoding check but it always looks for non-ASCII bytes.
# Encoding is used for display BUT it only really works for Single Byte encodings.
#

import os
import sys
import cgi
import urllib
import webbrowser

IS_PY2 = sys.version_info[0] == 2

#import cherrypy # http://www.cherrypy.org/
## rhubarb tart # http://rhubarbtart.org/
## PySite (not Pysite, note case) 
##      http://www.programmingforums.org/forum/f43-python/t9028-pysite-web-development-framework.html
##      http://www.programmingforums.org/thread9028.html
try:
    #raise(ImportError)
    import cherrypy
    from cherrypy.lib.static import serve_file
except ImportError:
    try:
        import dietcherrypy as cherrypy
        serve_file = cherrypy.serve_file
    except ImportError:
        cherrypy = None

############################
## TODO consider moving this into dietcherry
import inspect

def function_arg_list(object):
    """Simplistic method/function argument lister, returns list of strings. 
    Ignores "self" for object methods.
    """
    function_args = inspect.getargspec(object)[0]
    if inspect.ismethod(object):
        function_args = function_args[1:] ## ignore first argument, we assume it is "self"
    return function_args


def form_gen(function_object=None, post=None, text_message=None, url=None, default_values=None):
    """Generates a simple html form
    default_values should be a dict of param names
    """
    # doesn't use a proper template engine (and it probably should)
    if post is None:
        post = False
    if text_message is None:
        text_message="Please fill in the form and click the submit button"
    
    simple_template = """
<form action="%s" method="%s">
    %s
<br><br>

%s
    <input type="submit" />
</form>
"""    
    
    the_fields=''
    for arg in function_arg_list(function_object):
        def_val = ''
        if default_values:
            try:
                if default_values[arg] is not None:
                    def_val = default_values[arg]
            except KeyError:
                pass
            
        the_fields += '    %s: <input type="text" name="%s" value="%s"/><br>\n' % (arg, arg, def_val)
    
    if post:
        form_type="POST"
    else:
        form_type="GET"
    the_form = simple_template % (function_object.__name__, form_type, text_message, the_fields)
    return the_form

############################

def dumb_word_split(in_str):
    in_str=in_str.replace(b',', b' ');
    in_str=in_str.replace(b'.', b' ');
    in_str=in_str.replace(b'"', b' ');
    in_str=in_str.replace(b"'", b' ');
    return in_str.split()

def find_non_ascii(line_obj, expected_encoding=None, filename=None):
    """
    @param line_obj  - object that when iterated returns lines,
            e.g. list of strings, a file object
    
    @param expected_encoding what encoding is the file in?
    """
    print('expected_encoding:', expected_encoding)
    if IS_PY2:
        max_ascii = chr(126)
        max_ascii = chr(127)
    else:
        max_ascii = 127
    #print('using %r as max_ascii' % (max_ascii,))

    result = []
    data_count = 0
    extended_chars = {}
    
    filename = filename or 'unknown_file'
    for line_count, line in enumerate(line_obj):
        line_count += 1
        # read a line
        for x in line:
            # process line, byte at a time
            data_count += 1
            if x >= max_ascii:
                print_each_context=True
                if print_each_context:
                    if IS_PY2:
                        result.append('%s:%d: %3d %s @ %d' % (filename, line_count, ord(x), x, data_count))
                    else:
                        result.append('%s:%d: %3d %s @ %d' % (filename, line_count, x, x, data_count))  # TODO chr(x) before count
                    result.append(repr(line))
                    if IS_PY2:
                        result.append(line)
                    result.append('')
                try:
                    extended_chars[x] += 1
                except KeyError:
                    extended_chars[x] = 1
                #print('%3d' %(ord(x),) , x, '@', data_count)
    #print(len(line), line)
    #print(extended_chars)
    if extended_chars:
        result.append('========= character table =========')
        for x in extended_chars:
            if expected_encoding:
                try:
                    print(expected_encoding, repr(x))
                    if IS_PY2:
                        unicode_codepoint = x.decode(expected_encoding)
                    else:
                        unicode_codepoint = chr(x).encode(expected_encoding)  # not convinced this approach will work
                    unicode_codepoint_utf8=unicode_codepoint.encode('utf8')
                    unicode_codepoint=repr(unicode_codepoint)+' 0x%04x'%ord(unicode_codepoint)+' utf8:"'+unicode_codepoint_utf8+'" ('+repr(unicode_codepoint_utf8)+')'
                except UnicodeDecodeError:
                    #unicode_codepoint=''
                    unicode_codepoint='not valid %s character' % expected_encoding
                except UnicodeEncodeError:
                    unicode_codepoint='not valid %s character' % expected_encoding
            else:
                unicode_codepoint=''
            if IS_PY2:
                result.append('%3d 0x%x' % (ord(x),ord(x),)  + ' ' + unicode_codepoint + ' ' + x + ' ' + 'occurrences' + ' ' + str(extended_chars[x]))
            else:
                # FIXME by default sys.stdout defaults to utf-8 encoding (see sys.stdout.encoding) on all platforms
                # so chr(x) will result in unprintable characters under Windows
                result.append('%3d 0x%x' % (x, x,)  + ' ' + unicode_codepoint + ' ' + chr(x)  + ' ' + 'occurrences' + ' ' + repr(extended_chars[x]))
        result.append('=' * 65)
        result.append('')
    
    word_list = dumb_word_split(line)
    
    """
    word_count = 0
    print('debug', repr(line))
    for temp_word in word_list:
        #import pdb ; pdb.set_trace()
        for x in extended_chars:
            if x in temp_word:
                result.append(temp_word + ' ::: ' + '%3d 0x%x %s >%s<' %(ord(x), ord(x), repr(x), x))
                result.append('...' + ' '.join(word_list[word_count-2:word_count+2]) + '...')
        word_count += 1
    """
    print(repr(result))
    return '\n'.join(result)


class Root(object):
    def __init__(self):
        self.picdir = os.path.abspath(os.path.dirname(__file__))
        self.picdir = os.path.join(self.picdir, 'data')
    
    def index(self, string_data=None, expect_encoding='latin1'):
        if None in [string_data]:  # if None in all kwargs
            # from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66062
            this_function_name = sys._getframe().f_code.co_name
            this_function = getattr(self, this_function_name)
            #__result += form_gen(function_object=this_function, default_values=locals())
            __result =  '''<title>Unicode Dentist<title>
            
            <a href="http://www.imdb.com/title/tt0074860/quotes">is it safe?</a>
            </br>
<form action="index" method="GET">
    Please fill in the form and click the submit button
<br><br>

    expect_encoding: <input type="text" name="expect_encoding" value="latin1"/><br>
    string_data: <textarea name="string_data" value="" rows=20 cols=100></textarea><br>

    <input type="submit" />
</form>


            '''
            return __result
        print(repr(string_data[:10]))
        string_data = string_data.replace('\r', '')
        """
        if string_data[-1] != '\n':
            # code expects last line to end in eol
            string_data = string_data + '\n'
        """
        result = string_data
        result = find_non_ascii(string_data.split('\n'), expected_encoding=expect_encoding)
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return result
    index.exposed=True


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # nasty argv command line argument parsing
    print(repr(argv))
    print(len(argv))
    if len(argv) > 1:
        # Assume filename and optional encoding
        # no need for web server mode (file mode it more reliable, we have the raw bytes)
        filename = argv[1]
        try:
            expect_encoding = argv[2]
        except IndexError:
            expect_encoding = 'us-ascii'
        
        f = open(filename, 'rb')
        string_data = f.read()
        f.close()
        string_data = string_data.replace(b'\r', b'')  # NOTE universal new lines file mode would be better but not all implementations have this yet.....
        result = find_non_ascii(string_data.split(b'\n'), expected_encoding=expect_encoding, filename=filename)
        if result:
            if IS_PY2:
                print(result)
            else:  # py3
                print(repr(result))  # FIXME / TODO revisit
        else:
            print('%r is valid %s' % (filename, expect_encoding))
        return 0
    
    if cherrypy:
        print('cherrypy.__version__', cherrypy.__version__)
        
        class DumbOpt(object):
            pass
        opt = DumbOpt()
        opt.no_webbrowser = False
        server_name = 'localhost'  # TODO lookup hostname
        server_port = 8080
        
        """
        ## cherrypy v3 quickstart (no call backs allowed, need to thread locally)
        #cherrypy.quickstart(Root(form, self._webform_callback))
        
        ### cherrypy 3.0.2 does NOT have server.start_with_callback it is engine..?
        cherrypy.config.update({'server.socketPort':server_port})
        cherrypy.engine.start_with_callback(webbrowser.open, ('http://localhost:%d'%server_port,))
        """
        ### cherrypy 2.?.? (and dietcherypy)
        #cherrypy.config.update({'server.socketPort':server_port}) # maybe a 3.0 thing?
        cherrypy.config.update({'server.socket_port':server_port}) # CherryPy 3.1.2
        cherrypy.PERFORM_UTF8_DECODING_ON_URL_PARAMETERS = False
        mywebapp=Root()
        if opt.no_webbrowser:
            cherrypy.root=mywebapp
            cherrypy.server.start()
        else:
            # style start for:
            #   CherryPy 3.1 (tested with 3.1.2)
            #   dietcherypy
            def launch_webbrowser():
                url='http://%s:%d' % (server_name, server_port)
                webbrowser.open(url)
            cherrypy.engine.subscribe('start', launch_webbrowser) # CherryPy 3.1 api
            cherrypy.quickstart(mywebapp)


    return 0


if __name__ == "__main__":
    sys.exit(main())


