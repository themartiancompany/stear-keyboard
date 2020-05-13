# Stear Keyboard

[![Python 3.x Support](https://img.shields.io/pypi/pyversions/Django.svg)](https://python.org)
[![License: AGPL v3+](https://img.shields.io/badge/license-AGPL%20v3%2B-blue.svg)](http://www.gnu.org/licenses/agpl-3.0) 


*Stear Keyboard* is an extremely simple remote keyboard that runs on any platform on which you can install [GPG](https://gnupg.org) and Python.

It has mainly been written for the fictional do-it-yourself, n900-like, GNOME Mobile-powered smartphone *Stear Prime*, but it can pretty much be used everywhere.

*It is not recommended at this stage* (and probably never will) *to run it on public networks*, because even with encryption an attacker can still infer what are you writing from the keystroke sequences. That can of course be mitigated but I do not plan to do it soon.

## Installation

*Stear Keyboard* will soon be available through the [Python Package Index (PyPI)](https://pypi.org/). Pip is pre-installed if `python >= 3.4` has been downloaded from [python.org](https://python.org); if you're using a GNU/Linux distribution, you can find how to install it on this [page](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers).

After setting up pip, you will be able to install *Stear Keyboard* by simply typing in your terminal

    # pip3 install stear-keyboard

In the meantime, you can install it cloning this repository and running

    # sudo python3 setup.py install

## Usage

*Stear Keyboard* install a command line utility with the same name, `stear-keyboard`, which has to run on both the client (the device sharing the keyboard) and the server (the device receiving the input). At first run it will generate a GPG keyring with a default key having passphrase *test* in the user configuration directory. You will have to export (or copy) such keyring on the devices which have to interoperate. Of course you can add as many keys as you want.

```bash
# On server
stear-keyboard server test

# On client
stear-keyboard client stearkeyboard@arcipelago.ml <host>
```

You can invoke command line help with `stear-keyboard --help` and get command options with

    stear-keyboard <command> --help

The application requires `gpg` to be present on your system.

## About

This program is licensed under [GNU Affero General Public License v3 or later](https://www.gnu.org/licenses/gpl-3.0.en.html) by [Pellegrino Prevete](http://prevete.ml).<br>
If you find this program useful, consider offering me a [beer](https://patreon.com/tallero), a new [computer](https://patreon.com/tallero) or a part time remote [job](mailto:pellegrinoprevete@gmail.com) to help me pay the bills.


