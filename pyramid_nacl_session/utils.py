from binascii import unhexlify

from pyramid.session import JSONSerializer
from pyramid.session import PickleSerializer

from pyramid.settings import asbool

from .session import EncryptedCookieSessionFactory


def session_factory_from_settings(settings):
    """
    Return a Pyramid session factory using PyNaCl session settings
    supplied from a Paste configuration file.
    """

    prefixes = ("session.", "pynacl.session.")
    options = {}
    bool_options = {"secure", "httponly", "set_on_exception"}
    serializers = {"json": JSONSerializer, "pickle": PickleSerializer}

    # Pull out any config args meant for PyNaCl session, if there are any.
    for k, v in settings.items():
        for prefix in prefixes:
            if k.startswith(prefix):
                option_name = k[len(prefix) :]

                if option_name in bool_options:
                    v = asbool(v)
                elif option_name == "serializer":
                    if v in serializers:
                        v = serializers[v]()
                elif option_name == "secret":
                    if not isinstance(v, bytes):
                        v = unhexlify(v)

                options[option_name] = v

    return EncryptedCookieSessionFactory(**options)
