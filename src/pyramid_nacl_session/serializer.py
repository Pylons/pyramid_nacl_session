from base64 import urlsafe_b64decode
from base64 import urlsafe_b64encode
import binascii

from nacl.exceptions import CryptoError
from nacl.secret import SecretBox
from nacl.utils import random
from pyramid.session import JSONSerializer


class EncryptedSerializer(object):
    """Encrypt session state using PyNaCl.

    :type secret: bytes
    :param secret: a 32-byte random secret for encrypting/decrypting the
                   pickled session state.
    :param serializer:
        An object with two methods: ``loads`` and ``dumps``. The ``loads``
        method should accept bytes and return a Python object. The ``dumps``
        method should accept a Python object and return bytes. A ``ValueError``
        should be raised for malformed inputs. Default: ``None``, which will
        use :class:`pyramid.session.JSONSerializer`.
    """

    def __init__(self, secret, serializer=None):
        if len(secret) != SecretBox.KEY_SIZE:
            raise ValueError(
                "Secret should be a random bytes string of length {}".format(
                    SecretBox.KEY_SIZE
                )
            )
        self.box = SecretBox(secret)

        if serializer is None:
            serializer = JSONSerializer()

        self.serializer = serializer

    def loads(self, bstruct):
        """Decrypt session state.

        :type encrypted_state: bytes
        :param encrypted_state: the encrypted session state.

        :rtype: :class:`dict` / picklable mapping
        :returns: the decrypted, unpickled session state, as passed as
                  ``session_state`` to :meth:`dumps`.
        """
        try:
            b64padding = b"=" * (-len(bstruct) % 4)
            fstruct = urlsafe_b64decode(bstruct + b64padding)
        except (binascii.Error, TypeError) as e:
            raise ValueError("Badly formed base64 data: {}".format(e))
        try:
            payload = self.box.decrypt(fstruct)
        except CryptoError as e:
            raise ValueError("Possible tampering: {}".format(e))
        return self.serializer.loads(payload)

    def dumps(self, session_state):
        """Encrypt session state.

        :type session_state: :class:`dict` / picklable mapping
        :param session_state: the session state to be encrypted.

        :rtype: bytes
        :returns: the encrypted session state
        """
        cstruct = self.serializer.dumps(session_state)
        nonce = random(SecretBox.NONCE_SIZE)
        fstruct = self.box.encrypt(cstruct, nonce)
        return urlsafe_b64encode(fstruct).rstrip(b"=")
