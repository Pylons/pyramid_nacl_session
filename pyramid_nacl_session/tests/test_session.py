from pyramid import testing
import unittest
import webtest

class TestEncryptedCookieSessionFactory(unittest.TestCase):
    default_secret = b'seekrit!' * 4  # 32 bytes

    def _makeOne(self, **kw):
        from ..session import EncryptedCookieSessionFactory
        kw.setdefault('secret', self.default_secret)
        return EncryptedCookieSessionFactory(**kw)

    def test_it(self):
        config = testing.setUp()
        factory = self._makeOne()
        config.set_session_factory(factory)
        def begin_view(context, request):
            request.session['state'] = 1
            return 'begin'
        def end_view(context, request):
            self.assertEqual(request.session, {'state': 1})
            return 'end'
        config.add_view(begin_view, name='begin', renderer='string')
        config.add_view(end_view, name='end', renderer='string')
        app = config.make_wsgi_app()
        testapp = webtest.TestApp(app)

        testapp.get('/begin')
        testapp.get('/end')
        self.assertTrue('session' in testapp.cookies)
