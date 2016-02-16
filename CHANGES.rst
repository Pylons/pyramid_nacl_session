Changelog
=========

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
