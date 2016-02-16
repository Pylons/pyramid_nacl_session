Changelog
=========

0.3 (unreleased)
----------------

- Drop Python 3.2 support.

0.2 (2015-11-23)
----------------

- Split the ``EncryptingPickleSerializer`` into ``EncryptedSerializer``
  with a default dependency on ``pyramid.session.PickleSerializer`` allowing
  alternative serializers to be used with the encryption interface.
  See https://github.com/Pylons/pyramid_nacl_session/pull/4

0.1 (2015-11-23)
----------------

- Initial release.
