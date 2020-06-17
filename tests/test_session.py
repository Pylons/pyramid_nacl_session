import unittest
import webtest
from pyramid import testing


class SomeClass(object):
    pass


class TestEncryptedCookieSessionFactory(unittest.TestCase):
    default_secret = b"seekrit!" * 4  # 32 bytes

    def _makeOne(self, **kw):
        from pyramid_nacl_session.session import EncryptedCookieSessionFactory

        kw.setdefault("secret", self.default_secret)
        return EncryptedCookieSessionFactory(**kw)

    def _makeOneFromSettings(self, **kw):
        from pyramid_nacl_session.utils import session_factory_from_settings

        kw.setdefault("session.secret", self.default_secret)
        return session_factory_from_settings(kw)

    def test_cookie(self):
        test_secure = self._build_cookie({"session.secure": "true"})
        test_secure_prefix = self._build_cookie({"pynacl.session.secure": "true"})
        test_not_secure = self._build_cookie({"session.secure": "false"})
        test_http_only = self._build_cookie({"session.httponly": "true"})
        test_http_secure = self._build_cookie(
            {"pynacl.session.secure": "true", "session.httponly": "true"}
        )
        test_cookie_name = self._build_cookie({"session.cookie_name": "_test_"})
        test_samesite = self._build_cookie({"session.samesite": "Strict"})

        _session_data = {
            "k1": "v1",
            "k2": 1,
            "k3": [1, 2, 3],
            "k4": {"t1": "v1", "t2": "v2"},
            "foo": ("some", "key"),
        }

        self.assertIn("secure;", test_secure)
        self.assertIn("secure;", test_secure_prefix)
        self.assertNotIn("secure;", test_not_secure)
        self.assertIn("HttpOnly;", test_http_only)
        self.assertIn("HttpOnly;", test_http_secure)
        self.assertIn("secure;", test_http_secure)
        self.assertIn("_test_=", test_cookie_name)
        self.assertIn("SameSite=Lax", test_cookie_name)
        self.assertIn("SameSite=Strict", test_samesite)

        with self.assertRaises(ValueError):
            self._build_cookie({"session.secret": "invalid"})

        with self.assertRaises(TypeError):
            _not_serializable = _session_data.copy()
            _not_serializable["k5"] = SomeClass
            self._build_cookie({"session.serializer": "json"}, _not_serializable)

        _pickle_serializable = _session_data.copy()
        _pickle_serializable["k5"] = SomeClass()
        _pickle_serializable["k6"] = SomeClass

        self.assertTrue(
            self._build_cookie({"session.serializer": "pickle"}, _pickle_serializable)
        )

    def _build_cookie(self, kw, session_data=None):
        config = testing.setUp()
        factory = self._makeOneFromSettings(**kw)
        config.set_session_factory(factory)

        if session_data is None:
            session_data = {}

        def test_view(context, request):
            request.session.update(session_data)
            return "test"

        config.add_view(test_view, name="test", renderer="string")
        app = config.make_wsgi_app()
        testapp = webtest.TestApp(app)
        resp = testapp.get("/test")
        return resp.headers.get("set-cookie")

    def test_include_me(self):
        from pyramid.config import Configurator
        from pyramid.registry import Registry
        from pyramid.interfaces import ISessionFactory
        from pyramid_nacl_session import includeme

        settings = {"session.secret": self.default_secret}
        reg = Registry()
        config = Configurator(reg)
        config.add_settings(settings)
        config.include(includeme)
        config.commit()
        factory = self._makeOne()
        self.assertIs(type(config.registry.getUtility(ISessionFactory)), type(factory))

    def test_it(self):
        config = testing.setUp()
        factory = self._makeOne()
        config.set_session_factory(factory)
        state_found = []

        def begin_view(context, request):
            state_found.append(request.session.copy())
            request.session["state"] = 1
            return "begin"

        def end_view(context, request):
            state_found.append(request.session.copy())
            return "end"

        config.add_view(begin_view, name="begin", renderer="string")
        config.add_view(end_view, name="end", renderer="string")
        app = config.make_wsgi_app()
        testapp = webtest.TestApp(app)

        testapp.get("/begin")
        testapp.get("/end")
        self.assertTrue("session" in testapp.cookies)
        self.assertEqual(state_found[0], {})
        self.assertEqual(state_found[1], {"state": 1})
