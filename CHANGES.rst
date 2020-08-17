Changelog
=========

1.0.0 (2020-08-17)
------------------

- Add ``session_factory_from_settings`` and ``includeme``.
  See https://github.com/Pylons/pyramid_nacl_session/pull/11

- Support the ``samesite`` option and default to ``Lax``.
  See https://github.com/Pylons/pyramid_nacl_session/pull/14

- Drop Python 2.6, 3.3, and 3.4 support.

- Add Python 3.6, 3.7 and 3.8 support.

0.3 (2016-02-16)
----------------

- Drop Python 3.2 support.

- Drop the trailing padding (``=``) from base64 content.
  See https://github.com/Pylons/pyramid_nacl_session/pull/7

- Add the ``EncryptedCookieSessionFactory`` as the primary API for using
  an encrypted session.
  See https://github.com/Pylons/pyramid_nacl_session/pull/6

0.2 (2015-11-23)
----------------

- Split the ``EncryptingPickleSerializer`` into ``EncryptedSerializer``
  with a default dependency on ``pyramid.session.PickleSerializer`` allowing
  alternative serializers to be used with the encryption interface.
  See https://github.com/Pylons/pyramid_nacl_session/pull/4

0.1 (2015-11-23)
----------------

- Initial release.
