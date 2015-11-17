import unittest


class Test_generate_secret(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from ..scripts import generate_secret
        return generate_secret(*args, **kw)

    def test_it(self):
        from .. import scripts as MUT

        class _SecretBox(object):
            KEY_SIZE = 32

        def _random(size):
            return b'\x01\x12\x23\x34\x45'

        _wrote = []

        with _Monkey(MUT, SecretBox=_SecretBox, random=_random):
            secret = self._callFUT()
        self.assertEqual(secret, '0112233445')



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
