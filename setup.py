from setuptools import setup, find_packages
setup(
    name='MusicDownloader',
    version= 0.12,
    packages=find_packages(),
    description='Download MP3 through the ID of the song',
    author='Huni',
    author_email='huhuhuni@yeah.net',
    license='MIT',
    install_requires=[
        "requests",
        "bs4",
        "PyExecJS",
        "pycryptodome"
        ]
    )