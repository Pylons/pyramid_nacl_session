import unittest


class EncryptedSerializerTests(unittest.TestCase):
    def _getTargetClass(self):
        from pyramid_nacl_session.serializer import EncryptedSerializer

        return EncryptedSerializer

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _serialize(self, value, secret, nonce):
        import base64
        from pyramid.compat import pickle
        from nacl.secret import SecretBox

        cstruct = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        fstruct = SecretBox(secret).encrypt(cstruct, nonce)
        return base64.urlsafe_b64encode(fstruct).rstrip(b"=")

    def test_ctor_w_invalid_key(self):
        SECRET = b"SEEKRIT!"
        self.assertRaises(ValueError, self._makeOne, SECRET)

    def test_dumps(self):
        from pyramid_nacl_session import serializer as MUT

        SECRET = b"SEEKRIT!" * 4  # 32 bytes
        NONCE = b"\x01" * 24
        APPSTRUCT = {"foo": "bar"}
        expected = self._serialize(APPSTRUCT, SECRET, NONCE)

        eps = self._makeOne(SECRET)
        with _Monkey(MUT, random=lambda size: NONCE):
            encrypted = eps.dumps(APPSTRUCT)
        self.assertEqual(expected, encrypted)

    def test_loads(self):
        SECRET = b"SEEKRIT!" * 4  # 32 bytes
        NONCE = b"\x01" * 24
        APPSTRUCT = {"foo": "bar"}
        CIPHERTEXT = self._serialize(APPSTRUCT, SECRET, NONCE)

        eps = self._makeOne(SECRET)
        loaded = eps.loads(CIPHERTEXT)
        self.assertEqual(loaded, APPSTRUCT)

    def test_loads_with_invalid_b64(self):
        eps = self._makeOne(b"SEEKRIT!" * 4)
        self.assertRaises(ValueError, eps.loads, b"not*b64*data")

    def test_loads_with_tampered_content(self):
        import base64
        from pyramid.compat import pickle
        from nacl.secret import SecretBox

        secret = b"SEEKRIT!" * 4
        appstruct = {"foo": "bar"}
        nonce = b"\x01" * 24
        cstruct = pickle.dumps(appstruct, pickle.HIGHEST_PROTOCOL)
        fstruct = SecretBox(secret).encrypt(cstruct, nonce)
        fstruct = b"tamper" + fstruct
        bstruct = base64.urlsafe_b64encode(fstruct).rstrip(b"=")

        eps = self._makeOne(b"SEEKRIT!" * 4)
        self.assertRaises(ValueError, eps.loads, bstruct)


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
