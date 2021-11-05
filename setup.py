from setuptools import setup

setup(
    name='aiowikibot',
    version='0.0.3',
    packages=['aiowikibot'],
    install_requires=[
        'httpx',
        'asyncio',
        'ujson'
    ],
)