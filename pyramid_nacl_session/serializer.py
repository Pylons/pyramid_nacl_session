from nacl.secret import SecretBox
from nacl.utils import random
from pyramid.compat import pickle


class EncryptingPickleSerializer(object):

    def __init__(self, secret):
        if len(secret) != SecretBox.KEY_SIZE:
            raise ValueError(
                "Secret should be a random bytes string of length %d"
                    % SecretBox.KEY_SIZE)
        self.box = SecretBox(secret)

    def loads(self, ciphertext):
        payload = self.box.decrypt(ciphertext)
        return pickle.loads(payload)

    def dumps(self, appstruct):
        pickled = pickle.dumps(appstruct)
        nonce = random(SecretBox.NONCE_SIZE)
        return self.box.encrypt(pickled, nonce)

