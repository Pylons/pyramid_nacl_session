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
        state_found = []
        def begin_view(context, request):
            state_found.append(request.session.copy())
            request.session['state'] = 1
            return 'begin'
        def end_view(context, request):
            state_found.append(request.session.copy())
            return 'end'
        config.add_view(begin_view, name='begin', renderer='string')
        config.add_view(end_view, name='end', renderer='string')
        app = config.make_wsgi_app()
        testapp = webtest.TestApp(app)

        testapp.get('/begin')
        testapp.get('/end')
        self.assertTrue('session' in testapp.cookies)
        self.assertEqual(state_found[0], {})
        self.assertEqual(state_found[1], {'state': 1})
