Using ``pyramid_nacl_session``
==============================

Setup
-----

Once :mod:`pyramid_nacl_session` is installed, you typically use the 
``config.include`` mechanism to include it into your Pyramid project's 
configuration.

In your Pyramid project's ``__init__.py``:

.. code-block:: python

    with Configurator(settings=settings) as config:
        config.include('pyramid_nacl_session')
        # ... more config.includes
        config.scan()

Alternately, instead of using the Configurator's ``include`` method, you can 
activate :mod:`pyramid_nacl_session` by changing your application's ``.ini`` 
file, using the following line:

.. code-block:: ini

    pyramid.includes = pyramid_nacl_session

Usage
-----

Generate a secret key
^^^^^^^^^^^^^^^^^^^^^
To facilitate sharing the secret across instances, ``pyramid_nacl_session`` 
provides a ``print_secret`` script, which generates and hexlifies a random 
secret, printing it to standard output:

.. code-block:: bash

    $ bin/print_secret
    840aaafdc36f067fbad9baf006efc0f672b86ab0dcb6a3e43ecc1f9d760915e5

Cut-and-paste into your config file:

.. code-block:: ini

    session.secret =
        840aaafdc36f067fbad9baf006efc0f672b86ab0dcb6a3e43ecc1f9d760915e5

Session management
^^^^^^^^^^^^^^^^^^
If you have included :mod:`pyramid_nacl_session` in your Pyramid project's 
configuration as shown above then 
:func:`pyramid_nacl_session.session_factory_from_settings` is called 
automatically and you need do nothing else.

Otherwise you will need to create a Pyramid :term:`session factory` by adding a 
call to either the :func:`pyramid_nacl_session.EncryptedCookieSessionFactory` 
function or the :func:`pyramid_nacl_session.session_factory_from_settings` 
function in the configuration code of your Pyramid project's ``__init__.py`` 
file and subsequently register that session factory with Pyramid.

At that point, accessing ``request.session`` will provide a Pyramid session 
using PyNaCl as a backend.

:func:`pyramid_nacl_session.session_factory_from_settings` obtains session 
settings from the ``**settings`` dictionary passed to the Configurator.
It assumes that you've placed session configuration parameters prefixed with 
``session.`` in your Pyramid application's ``.ini`` file.  

For example:

.. code-block:: ini

    [app:myapp]
    # other settings 
    session.secret = 840aaafdc36f067fbad9baf006efc0f672b86ab0dcb6a3e43ecc1f9d760915e5
    session.serializer = json

If your ``.ini`` file has such settings, you can use 
:func:`pyramid_nacl_session.session_factory_from_settings` in your 
application's configuration.

For example, let's assume this code is in the ``__init__.py`` of your Pyramid 
application that uses an ``.ini`` file with the ``session.`` settings above to 
obtain its ``**settings`` dictionary.

.. code-block:: python

    from pyramid_nacl_session import session_factory_from_settings
    from pyramid.config import Configurator

    def app(global_config, **settings):
        """ This function returns a WSGI application.

        It is usually called by the PasteDeploy framework during 
        ``paster serve``.
        """
        session_factory = session_factory_from_settings(settings)
        with Configurator(settings=settings) as config:
            config.set_session_factory(session_factory)
            # other configuration stuff
            return config.make_wsgi_app()
