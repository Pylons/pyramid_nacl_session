import binascii
import getopt
import sys

from nacl.secret import SecretBox
from nacl.utils import random


def generate_secret():
    return binascii.hexlify(random(SecretBox.KEY_SIZE))


PRINT_SECRET_DOC = """\
Print a generated, random secret, to standard output.

The secret is a 32-byte random string, encoded using 'binascii.hexlify'.
"""
def print_secret():  # pragma: NO COVER
    def _usage(message=None, rc=1):
        print(PRINT_SECRET_DOC)
        if message is not None:
            print(message)
        sys.exit(rc)

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], '?h', ['help'])
    except getopt.GetoptError as e:
        _usage(str(e))

    if args:
        _usage('No arguments allowed.')

    for k, v in opts:
        if k in ('-?', '-h', '--help'):
            _usage(rc=2)

    print(generate_secret())
