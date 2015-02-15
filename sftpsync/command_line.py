import sys
from sys import argv, exit
import os
from os import linesep
from getopt import getopt, GetoptError


ERROR_ILLEGAL_ARGUMENTS = 2

def usage(error_message=None):
    if error_message:
        sys.stderr.write('ERROR: ' + error_message + linesep)

    sys.stdout.write(linesep.join([
        'Usage:',
        '    sftpsync.py [OPTION]... SOURCE DESTINATION',
        'Pull:',
        '    sftpsync.py [OPTION]... [user[:password]@]host[:[port]/path] /path/to/local/copy',
        'Push:',
        '    sftpsync.py [OPTION]... /path/to/local/copy [user[:password]@]host[:[port]/path]',
        linesep,
        'Defaults:',
        '    user:     anonymous',
        '    password: anonymous',
        '    port:     22',
        '    path:     /',
        linesep,
        'Options:',
        '-f/--force      Force the synchronization regardless of files\' presence or timestamps.',
        '-h/--help       Prints this!',
        '-i/--identity identity_file',
        '                Selects the file from which the identity (private key) for public key authentication is read.',
        '-o ssh_option',
        '                Can be used to pass options to ssh in the format used in ssh_config(5). This is useful for specifying options for which there is no separate sftpsync command-line flag.',
        '                For full details of the options listed below, and their possible values, see ssh_config(5).',
        '                    ProxyCommand',
        '-p/--preserve:  Preserves modification times, access times, and modes from the original file.',
        '--proxy [user[:password]@]host[:port]',
        '                SOCKS proxy to use. If not provided, port will be defaulted to 1080.',
        '--proxy-version SOCKS4|SOCKS5',
        '                Version of the SOCKS protocol to use. Default is SOCKS5.',
        '-q/--quiet:     Quiet mode: disables the progress meter as well as warning and diagnostic messages from ssh(1).',
        '-r/--recursive: Recursively synchronize entire directories.',
        '-v/--verbose:   Verbose mode. Causes sftpsync to print debugging messages about their progress. This is helpful in debugging connection, authentication, and configuration problems.',
        linesep
    ]))

def configure(argv):
    try:
        # Default configuration:
        config = {
            'force':     False,
            'preserve':  False,
            'quiet':     False,
            'recursive': False,
            'verbose':   False,
            'private-key':  None,
        }

        opts, args = getopt(argv, 'fhi:pqrv', ['force', 'help', 'identity=', 'preserve', 'quiet', 'recursive', 'verbose'])
        for opt, value in opts:
            if opt in ('-h', '--help'):
                usage()
                exit()
            if opt in ('-f', '--force'):
                config['force']     = True
            if opt in ('-p', '--preserve'):
                config['preserve']  = True
            if opt in ('-q', '--quiet'):
                config['quiet']     = True
            if opt in ('-r', '--recursive'):
                config['recursive'] = True
            if opt in ('-v', '--verbose'):
                config['verbose']   = True
            if opt in ('-i', '--identity'):
                config['private-key'] = _validate_private_key_path(value)

        if config['verbose'] and config['quiet']:
            raise ValueError('Please provide either -q/--quiet OR -v/--verbose, but NOT both at the same time.')

        return config
    except GetoptError as e:
        usage(str(e))
        exit(ERROR_ILLEGAL_ARGUMENTS)
    except ValueError as e:
        usage(str(e))
        exit(ERROR_ILLEGAL_ARGUMENTS)

def _validate_private_key_path(path):
    if not path:
        raise ValueError('Invalid path: "%s". Please provide a valid path to your private key.' % path)
    if not os.path.exists(path):
        raise ValueError('Invalid path. "%s" does NOT exist. Please provide a valid path to your private key.' % path)
    return path
