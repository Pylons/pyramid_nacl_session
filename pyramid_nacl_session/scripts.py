import binascii
import getopt
import sys

from nacl.secret import SecretBox
from nacl.utils import random


def generate_secret(as_hex=True):
    """Generate a random, 32-byte secret.

    :type as_hex: boolean
    :param as_hex: If true, convert the secret to hex.

    :rtype: bytes
    :returns: the secret (perhaps converted to hex).
    """
    secret = random(SecretBox.KEY_SIZE)
    if as_hex:
        secret = binascii.hexlify(secret)
    return secret


def print_secret():  # pragma: NO COVER
    """Print a generated, random secret, to standard output.

    The secret is a 32-byte random string, encoded using
    :func:`binascii.hexlify`.
    """
    def _usage(message=None, rc=1):
        print(print_secret.__doc__)
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
