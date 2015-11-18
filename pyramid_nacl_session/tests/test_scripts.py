import unittest


class Test_generate_secret(unittest.TestCase):

    RANDOM = b'\x01\x12\x23\x34\x45'

    def _callFUT(self, *args, **kw):
        from ..scripts import generate_secret
        return generate_secret(*args, **kw)

    def test_implicit(self):
        from binascii import hexlify
        from .. import scripts as MUT

        class _SecretBox(object):
            KEY_SIZE = 32

        def _random(size):
            return self.RANDOM

        with _Monkey(MUT, SecretBox=_SecretBox, random=_random):
            secret = self._callFUT()

        self.assertEqual(secret, hexlify(self.RANDOM))

    def test_explicit(self):
        from .. import scripts as MUT

        class _SecretBox(object):
            KEY_SIZE = 32

        def _random(size):
            return self.RANDOM

        with _Monkey(MUT, SecretBox=_SecretBox, random=_random):
            secret = self._callFUT(as_hex=False)

        self.assertEqual(secret, self.RANDOM)



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
