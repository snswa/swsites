from setuptools import setup, find_packages


setup(
    name = "swproject",
    version = "1.0",
    author = "ElevenCraft Inc. and contributors",
    author_email = "webmaster@sensiblewashington.org",
    description = "",
    long_description = "", #open("README").read(),
    license = "Apache 2.0",
    url = "http://sensiblewashington.org/",
    packages = find_packages(exclude=[
        'conf',
        'dev',
        'production',
        'uploaded_media',
    ]),
    classifiers = [
    ]
)
