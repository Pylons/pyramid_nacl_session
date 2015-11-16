import struct

from pyramid.compat import pickle

try:
    from Crypto import Random
except ImportError:
    _HAS_CRYPTO = False
else:
    _HAS_CRYPTO = True
    from Crypto.Cipher import Blowfish
    BLOCK_SIZE = Blowfish.block_size
    IV = Random.new().read(BLOCK_SIZE)


class EncryptingPickleSerializer(object):

    def __init__(self, secret):
        self.secret = secret

    def loads(self, bstruct):
        iv, payload = bstruct[:BLOCK_SIZE], bstruct[BLOCK_SIZE:]
        cipher = Blowfish.new(self.secret, Blowfish.MODE_CBC, iv)
        payload = cipher.decrypt(payload)
        return pickle.loads(payload)

    def dumps(self, appstruct):
        pickled = pickle.dumps(appstruct)
        # For an explanation / example of the padding, see:
        # https://www.dlitz.net/software/pycrypto/api/current/\
        # Crypto.Cipher.Blowfish-module.html
        plen = BLOCK_SIZE - divmod(len(pickled), BLOCK_SIZE)[1]
        padding = struct.pack('b' * plen, *([plen] * plen))
        cipher = Blowfish.new(self.secret, Blowfish.MODE_CBC, IV)
        return IV + cipher.encrypt(pickled + padding)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.secret == other.secret

