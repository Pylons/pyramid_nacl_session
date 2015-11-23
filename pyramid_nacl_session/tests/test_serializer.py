import unittest


class EncryptedSerializerTests(unittest.TestCase):

    def _getTargetClass(self):
        from ..serializer import EncryptedSerializer
        return EncryptedSerializer

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_w_invalid_key(self):
        SECRET = 'SEEKRIT!'
        self.assertRaises(ValueError, self._makeOne, SECRET)

    def test_dumps(self):
        from pyramid.compat import pickle
        from .. import serializer as MUT
        SECRET = 'SEEKRIT!' * 4  # 32 bytes
        NONCE = b'\x01' * 24
        APPSTRUCT = {'foo': 'bar'}
        PICKLED = pickle.dumps(APPSTRUCT, pickle.HIGHEST_PROTOCOL)
        _base64_called = []
        def _base64_encode(what):
            _base64_called.append(what)
            return what
        with _Monkey(MUT,
                     SecretBox=_SecretBox,
                     random=lambda size: NONCE,
                     urlsafe_b64encode=_base64_encode):
            eps = self._makeOne(SECRET)
            encrypted = eps.dumps(APPSTRUCT)
            pickled, nonce = encrypted[:-25], encrypted[-24:]
            self.assertEqual(pickled, PICKLED)
            self.assertEqual(nonce, NONCE)
            self.assertEqual(_base64_called, [encrypted])

    def test_loads(self):
        from pyramid.compat import pickle
        from .. import serializer as MUT
        SECRET = 'SEEKRIT!' * 4  # 32 bytes
        NONCE = b'\x01' * 24
        APPSTRUCT = {'foo': 'bar'}
        PICKLED = pickle.dumps(APPSTRUCT, pickle.HIGHEST_PROTOCOL)
        CIPHERTEXT = PICKLED + b':' + NONCE
        _base64_called = []
        def _base64_decode(what):
            _base64_called.append(what)
            return what
        with _Monkey(MUT, SecretBox=_SecretBox,
                     urlsafe_b64decode=_base64_decode):
            eps = self._makeOne(SECRET)
            loaded = eps.loads(CIPHERTEXT)
            self.assertEqual(loaded, APPSTRUCT)
            self.assertEqual(_base64_called, [CIPHERTEXT])


class _SecretBox(object):

    KEY_SIZE = 32
    NONCE_SIZE = 24

    def __init__(self, key):
        assert len(key) == self.KEY_SIZE
        self._key = key

    def encrypt(self, plaintext, nonce):
        assert len(nonce) == self.NONCE_SIZE
        return plaintext + b':' + nonce

    def decrypt(self, ciphertext):
        return ciphertext[:-(self.NONCE_SIZE + 1)]


class _Monkey(object):
    # context-manager for replacing module names in the scope of a test.

    def __init__(self, module, **kw):
        self.module = module
        self.to_restore = dict([(key, getattr(module, key)) for key in kw])
        for key, value in kw.items():
            setattr(module, key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key, value in self.to_restore.items():
            setattr(self.module, key, value)
