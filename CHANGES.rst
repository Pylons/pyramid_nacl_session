Changelog
=========

0.2 (unreleased)
----------------

- Split the ``EncryptingPickleSerializer`` into ``EncryptedSerializer``
  with a default dependency on ``pyramid.session.PickleSerializer`` allowing
  alternative serializers to be used with the encryption interface.
  See https://github.com/Pylons/pyramid_nacl_session/pull/4

0.1 (2015-11-23)
----------------

- Initial release.
