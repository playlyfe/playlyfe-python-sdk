from setuptools import setup, find_packages
setup(
  name = 'playlyfe',
  version = '0.1.1',
  packages= ['src'],
  description='This is the official OAuth 2.0 Python client SDK for the Playlyfe API',
  long_description='''
    It supports the client_credentials and authorization code OAuth 2.0 flows.
    For a complete API Reference checkout [Playlyfe Developers](https://dev.playlyfe.com/docs/api) for more information.
  ''',
  url='https://github.com/playlyfe/playlyfe-python-sdk',
  author='Peter John',
  author_email='peter@playlyfe.com',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7'
  ],
  keywords='REST, Playlyfe API, Playlyfe SDK, Gamification'
)

#python setup.py bdist_wheel
#twine upload dist/* -p password
