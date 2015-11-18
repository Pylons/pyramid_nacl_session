from base64 import urlsafe_b64decode
from base64 import urlsafe_b64encode

from nacl.secret import SecretBox
from nacl.utils import random
from pyramid.compat import pickle


class EncryptingPickleSerializer(object):
    """Encrypt pickled session state using PyNaCl.

    :type secret: bytes
    :param secret: a 32-byte random secret for encrypting/decrypting the
                   pickled session state.
    """
    def __init__(self, secret):
        if len(secret) != SecretBox.KEY_SIZE:
            raise ValueError(
                "Secret should be a random bytes string of length %d"
                    % SecretBox.KEY_SIZE)
        self.box = SecretBox(secret)

    def loads(self, encrypted_state):
        """Decrypt session state.

        :type encrypted_state: bytes
        :param encrypted_state: the encrypted session state.

        :rtype: :class:`dict` / picklable mapping
        :returns: the decrypted, unpickled session state, as passed as
                  ``session_state`` to :meth:`dumps`.
        """
        payload = self.box.decrypt(urlsafe_b64decode(encrypted_state))
        return pickle.loads(payload)

    def dumps(self, session_state):
        """Encrypt session state.

        :type session_state: :class:`dict` / picklable mapping
        :param session_state: the session state to be encrypted.

        :rtype: bytes
        :returns: the encrypted session state
        """
        pickled = pickle.dumps(session_state)
        nonce = random(SecretBox.NONCE_SIZE)
        return urlsafe_b64encode(self.box.encrypt(pickled, nonce))

