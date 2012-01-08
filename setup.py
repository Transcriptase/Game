try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'A simple text adventure to help me learn Python',
    'author': 'Russell Williams',
    'url':'https://github.com/Transcriptase/Game',
    'download': 'https://github.com/Transcriptase/Game',
    'author_email': 'russell.d.williams@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages':['Game'],
    'scripts':[],
    'name': 'Game'
}

setup(**config)