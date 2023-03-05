# coding: latin-1

###############################################################################
# eVotUM - Electronic Voting System
#
# pkiutils.py
#
# Cripto-5.0.0 - Public Key cryptography Functions
#
# Copyright (c) 2016 Universidade do Minho
# Developed by André Baptista - Devise Futures, Lda. (andre.baptista@devisefutures.com)
#
# Reviewed and tested with Python 3 @Jan/2021 by
#      José Miranda - Devise Futures, Lda. (jose.miranda@devisefutures.com)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
###############################################################################

import os
from setuptools import setup


def read(fname):   # Utility function to read the README file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="evotum-cripto",
    version="2.0",
    author="André Baptista",
    author_email="info@devisefutures.com",
    description=("eVotUM Cripto"),
    license="GNU GPL-3.0",
    keywords="electronic vote crypto",
    url="https://gitlab.com/eVotUM/Cripto-py",
    packages=["eVotUM", "eVotUM/Cripto"],
    long_description=read("README"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    install_requires=[
        "colored==1.4.2",
        "pyopenssl>=19.1.0,<=20.0.1",
        "utilitybelt==0.2.6",
        "six==1.15.0",
        "pycryptodome==3.9.9",
        "argon2-cffi==20.1.0"
    ],
)
