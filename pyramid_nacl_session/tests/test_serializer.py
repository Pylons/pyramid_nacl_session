import unittest


class EncryptingPickleSerializerTests(unittest.TestCase):

    def _getTargetClass(self):
        from ..serializer import EncryptingPickleSerializer
        return EncryptingPickleSerializer

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        SECRET = 'SEEKRIT'
        eps = self._makeOne(SECRET)
        self.assertEqual(eps.secret, SECRET)

    def test_dumps_short(self):
        from pyramid.compat import pickle
        from .. import serializer as MUT
        SECRET = 'SEEKRIT'
        IV = 'ABCDEFGH'
        APPSTRUCT = {}
        PICKLED = pickle.dumps(APPSTRUCT)
        with _Monkey(MUT,
                     _HAS_CRYPTO=True,
                     Blowfish=_Blowfish,
                     BLOCK_SIZE=8,
                     IV=IV,
                    ):
            eps = self._makeOne(SECRET)
            iv_encrypted = eps.dumps(APPSTRUCT)
            iv, encrypted = iv_encrypted[:8], iv_encrypted[8:]
            self.assertEqual(iv, IV)
            self.assertTrue(encrypted.startswith(PICKLED))
            self.assertEqual(len(encrypted) % 8, 0)

    def test_dumps_longer(self):
        from pyramid.compat import pickle
        from .. import serializer as MUT
        SECRET = 'SEEKRIT'
        IV = 'ABCDEFGH'
        APPSTRUCT = {'foo': 'bar', 'baz': 1}
        PICKLED = pickle.dumps(APPSTRUCT)
        with _Monkey(MUT,
                     _HAS_CRYPTO=True,
                     Blowfish=_Blowfish,
                     BLOCK_SIZE=8,
                     IV=IV,
                    ):
            eps = self._makeOne(SECRET)
            iv_encrypted = eps.dumps(APPSTRUCT)
            iv, encrypted = iv_encrypted[:8], iv_encrypted[8:]
            self.assertEqual(iv, IV)
            self.assertTrue(encrypted.startswith(PICKLED))
            self.assertEqual(len(encrypted) % 8, 0)

    def test_loads_short(self):
        from pyramid.compat import pickle
        from .. import serializer as MUT
        SECRET = 'SEEKRIT'
        IV = 'ABCDEFGH'
        APPSTRUCT = {}
        PICKLED = pickle.dumps(APPSTRUCT)
        PLEN = len(PICKLED) % 8
        with _Monkey(MUT,
                     _HAS_CRYPTO=True,
                     Blowfish=_Blowfish,
                     BLOCK_SIZE=8,
                    ):
            eps = self._makeOne(SECRET)
            loaded = eps.loads(IV + PICKLED + 'x' * PLEN)
            self.assertEqual(loaded, APPSTRUCT)

    def test_loads_longer(self):
        from pyramid.compat import pickle
        from .. import serializer as MUT
        SECRET = 'SEEKRIT'
        IV = 'ABCDEFGH'
        APPSTRUCT = {'foo': 'bar', 'baz': 1}
        PICKLED = pickle.dumps(APPSTRUCT)
        PLEN = len(PICKLED) % 8
        with _Monkey(MUT,
                     _HAS_CRYPTO=True,
                     Blowfish=_Blowfish,
                     BLOCK_SIZE=8,
                    ):
            eps = self._makeOne(SECRET)
            loaded = eps.loads(IV + PICKLED + 'x' * PLEN)
            self.assertEqual(loaded, APPSTRUCT)


class _Blowfish(object):

    MODE_CBC = 1

    @classmethod
    def new(cls, secret, mode, iv):
        return cls()

    def encrypt(self, plaintext):
        return plaintext

    def decrypt(self, encrypted):
        return encrypted


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
