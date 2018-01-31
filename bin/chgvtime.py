#!/usr/bin/env /awips2/python/bin/python
"""Get and set attributes on a satellite netcdf file."""

import argparse
import os

# import numpy
from Scientific.IO import NetCDF

def _process_command_line():
    """Process the command line arguments.

    Return an argparse.parse_args namespace object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--seconds', action='store', default='0', type=int,
        help='file valid time'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='verbose flag'
    )
    parser.add_argument(
        '-f', '--filepath', action='store', required=True,
        help='netCDF file path'
    )
    args = parser.parse_args()
    return args

def main():
    """Call to run script."""
    args = _process_command_line()
    if not os.path.exists(args.filepath):
        print 'File not found: {}'.format(args.filepath)
        raise SystemExit
    try:
        if args.verbose:
            print 'Opening {}'.format(args.filepath)
        cdf_fh = NetCDF.NetCDFFile(args.filepath, 'a')
    except IOError:
        print 'Error accessing {}'.format(args.filepath)
        raise SystemExit
    except OSError:
        print 'Error accessing {}'.format(args.filepath)
        raise SystemExit

    tvar = cdf_fh.variables['validTime']
    if args.seconds > 0:
        tvar.assignValue(args.seconds)
        print 'validTime changed to {}'.format(args.seconds)
    else:
        filesecs = tvar.getValue()
        print 'File validTime is {}'.format(filesecs)
    cdf_fh.close()
    return

if __name__ == '__main__':
    main()
