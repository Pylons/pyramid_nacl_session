from setuptools import find_packages
from setuptools import setup


with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

tests_require = []

setup(name='pyramid_nacl_session',
      version='0.2',
      description='Encrypted sessison cookie serializer ofr Pyramid',
      long_description='\n\n'.join([README, CHANGES]),
      url='https://github.com/Pylons/pyramid_nacl_session',
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: Repoze Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Topic :: Security :: Cryptography",
      ],
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
        'pyramid>=1.5',
        'PyNaCl',
      ],
      extras_require={
          'testing': tests_require + [
              'nose',
              'coverage',
          ],
          'docs': [
              'Sphinx',
              'pylons-sphinx-themes',
          ],
      },
      test_suite='pyramid_nacl_session.tests',
      tests_require=tests_require,
      entry_points = """\
      [console_scripts]
      print_secret = pyramid_nacl_session.scripts:print_secret
      """
)
