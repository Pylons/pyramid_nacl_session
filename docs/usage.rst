Using ``pyramid_nacl_session``
==============================

Generating a Random Secret
--------------------------

First, you need to arrange to have a 32-byte random secret available:

.. code-block:: python

   from pyramid_nacl_session import generate_secret

   SECRET = generate_secret(as_hex=False)

Configure a Session Factory
---------------------------

Use the generated secret to configure a session factory:

.. code-block:: python

   from pyramid.session import BaseCookieSessionFactory
   from pyramid_nacl_session import EncryptedSerializer

   def includeme(config):
       serializer = EncryptedSerializer(SECRET)
       factory = BaseCookieSessionFactory(serializer)  # other config ad lib.
       config.set_session_factory(factory)

Sharing the Secret Across Instances
-----------------------------------

To facilitate sharing the secret across instances, ``pyramid_nacl_session``
provides a ``print_secret`` script, which generates and hexlifies a random
secret, printing it to standard output:

.. code-block:: bash

   $ bin/print_secret
   840aaafdc36f067fbad9baf006efc0f672b86ab0dcb6a3e43ecc1f9d760915e5

Cut-and-paste into your config file:

.. code-block:: ini

   yourapp.session_secret =
      840aaafdc36f067fbad9baf006efc0f672b86ab0dcb6a3e43ecc1f9d760915e5

Parse the secret from the configuration, de-hexlify it, and use it to
construct and register a session factory:

.. code-block:: python

   import binascii
   from pyramid.session import BaseCookieSessionFactory
   from pyramid_nacl_session import EncryptedSerializer

   def includeme(config):
       hex_secret = config.settings['yourapp.session_secret'].strip()
       secret = binascii.unhexlify(hex_secret)
       serializer = EncryptedSerializer(secret)
       factory = BaseCookieSessionFactory(serializer)  # other config ad lib.
       config.set_session_factory(factory)

