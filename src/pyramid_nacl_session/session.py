from pyramid.session import (
    BaseCookieSessionFactory,
    PickleSerializer,
)

from .serializer import EncryptedSerializer


def EncryptedCookieSessionFactory(
    secret,
    cookie_name="session",
    max_age=None,
    path="/",
    domain=None,
    secure=False,
    httponly=False,
    timeout=1200,
    reissue_time=0,
    set_on_exception=True,
    serializer=None,
    samesite="Lax",
):
    """
    Configure a :term:`session factory` which will provide encrypted
    cookie-based sessions.  The return value of this
    function is a :term:`session factory` which may be used with the
    :meth:`pyramid.config.Configurator.set_session_factory` method.

    The session factory returned by this function will create sessions
    which are limited to storing fewer than 4000 bytes of data (as the
    payload must fit into a single cookie).

    Parameters:

    ``secret``
      A string which is used to sign the cookie. The secret should be at
      least as long as the block size of the selected hash algorithm. For
      ``sha512`` this would mean a 128 bit (64 character) secret.  It should
      be unique within the set of secret values provided to Pyramid for
      its various subsystems (see :ref:`admonishment_against_secret_sharing`).

    ``cookie_name``
      The name of the cookie used for sessioning. Default: ``'session'``.

    ``max_age``
      The maximum age of the cookie used for sessioning (in seconds).
      Default: ``None`` (browser scope).

    ``path``
      The path used for the session cookie. Default: ``'/'``.

    ``domain``
      The domain used for the session cookie.  Default: ``None`` (no domain).

    ``secure``
      The 'secure' flag of the session cookie. Default: ``False``.

    ``httponly``
      Hide the cookie from Javascript by setting the 'HttpOnly' flag of the
      session cookie. Default: ``False``.

    ``samesite``
      The 'samesite' option of the session cookie. Set the value to ``None``
      to turn off the samesite option.  Default: ``'Lax'``.

    ``timeout``
      A number of seconds of inactivity before a session times out. If
      ``None`` then the cookie never expires. This lifetime only applies
      to the *value* within the cookie. Meaning that if the cookie expires
      due to a lower ``max_age``, then this setting has no effect.
      Default: ``1200``.

    ``reissue_time``
      The number of seconds that must pass before the cookie is automatically
      reissued as the result of accessing the session. The
      duration is measured as the number of seconds since the last session
      cookie was issued and 'now'.  If this value is ``0``, a new cookie
      will be reissued on every request accessing the session. If ``None``
      then the cookie's lifetime will never be extended.
      A good rule of thumb: if you want auto-expired cookies based on
      inactivity: set the ``timeout`` value to 1200 (20 mins) and set the
      ``reissue_time`` value to perhaps a tenth of the ``timeout`` value
      (120 or 2 mins).  It's nonsensical to set the ``timeout`` value lower
      than the ``reissue_time`` value, as the ticket will never be reissued.
      However, such a configuration is not explicitly prevented.
      Default: ``0``.

    ``set_on_exception``
      If ``True``, set a session cookie even if an exception occurs
      while rendering a view. Default: ``True``.

    ``serializer``
      An object with two methods: ``loads`` and ``dumps``.  The ``loads``
      method should accept bytes and return a Python object.  The ``dumps``
      method should accept a Python object and return bytes.  A ``ValueError``
      should be raised for malformed inputs.  If a serializer is not passed,
      the :class:`pyramid.session.PickleSerializer` serializer will be used.
    """
    if serializer is None:
        serializer = PickleSerializer()

    encrypted_serializer = EncryptedSerializer(secret, serializer=serializer,)

    return BaseCookieSessionFactory(
        encrypted_serializer,
        cookie_name=cookie_name,
        max_age=max_age,
        path=path,
        domain=domain,
        secure=secure,
        httponly=httponly,
        timeout=timeout,
        reissue_time=reissue_time,
        set_on_exception=set_on_exception,
        samesite=samesite,
    )
