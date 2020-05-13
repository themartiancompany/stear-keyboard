from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "stear-keyboard",
    version = "0.1",
    author = "Pellegrino Prevete",
    author_email = "pellegrinoprevete@gmail.com",
    description = "A remote keyboard for use in the Stear Prime smartphone",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.gnome.org/tallero/stear-keyboard",
    packages = find_packages(),
    package_data = {
    },
    entry_points = {
        'console_scripts': ['stear-keyboard = stear_keyboard:main']
    },
    install_requires = [
    'appdirs',
    'keyboard',
    'python-gnupg',
    'setproctitle',
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: Unix",
    ],
)
