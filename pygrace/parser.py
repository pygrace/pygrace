#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @uqfoundation)
# Author: Daniel Stouffer (daniel @stoufferlab.org)
# Copyright (c) 2013 Daniel Stouffer.
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
#
import sys
import optparse

__all__ = ['XYParser']

class XYParser(optparse.OptionParser):

    def __init__(self, *args, **kwargs):
        optparse.OptionParser.__init__(self, *args, **kwargs)

        # add all options
        self.add_option('-p', '--pipe', dest='is_pipe', action='store_true',
                          help='explicity tell to read input from standard in')
        self.add_option('-t', '--type', dest='data_type', type='str',
                          help="load the input as this type ['%default']")
        self.add_option('-d', '--delimiter', dest='delimiter', type='str',
                          help="split the input lines on this ['%default']")

        self.supported_types = {
            'float': float,
            'int': int,
            'long': int,
            'complex': complex,
            }

        # set defaults here than doing in the option to avoid conflicts
        self.set_defaults(
            is_pipe = False,
            data_type = 'float',
            delimiter = None,
            )

    def parse_args(self, *args, **kwargs):
        
        options, args = optparse.OptionParser.parse_args(self, *args, **kwargs)

        # convert string that is passed on command line to data type
        try:
            data_type = self.supported_types[options.data_type]
        except KeyError:
            message = "'%s' is not an allowed data type" % options.data_type
            raise self.error(message)

        # read the input stream
        if (not sys.stdin.isatty()) or options.is_pipe:
            inStream = sys.stdin

        else:
            # raise parser error if neither a pipe nor an filename is given
            try:
                filename = args[0]
            except IndexError:
                message = 'neither a pipe nor an input filename was given'
                self.error(message)

            inStream = open(filename)

        lineList = [line.strip() for line in inStream]
        inStream.close()

        # coerce the input lines into the data type
        result = []
        for line in lineList:
            x, y = line.split(options.delimiter)
            x, y = data_type(x), data_type(y)
            result.append( (x, y) )

        return options, result
