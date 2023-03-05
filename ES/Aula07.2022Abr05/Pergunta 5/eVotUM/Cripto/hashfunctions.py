# coding: latin-1

###############################################################################
# eVotUM - Electronic Voting System
#
# hashfunctions.py
#
# Cripto-6.0.0 - Hash Functions
#
# Copyright (c) 2016 Universidade do Minho
# Developed by André Baptista - Devise Futures, Lda. (andre.baptista@devisefutures.com)
# Reviewed by Ricardo Barroso - Devise Futures, Lda. (ricardo.barroso@devisefutures.com)
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

"""
A hash function is any function that can be used to map data of arbitrary size to
data of fixed size. The values returned by a hash function are called hash values,
hash codes or simply hashes.

A cryptographic hash function allows one to easily verify that some input data maps
to a given hash value, but if the input data is unknown, it is deliberately difficult
to reconstruct it (or equivalent alternatives) by knowing the stored hash value. This
is used for assuring integrity of transmitted data, and is the building block for
HMACs, which provide message authentication.

Some standard applications that employ hash functions include authentication, message
integrity, message fingerprinting, data corruption detection, and digital signature
efficiency.

For more information, please visit https://en.wikipedia.org/wiki/Hash_function.
"""

from Crypto.Hash import SHA256

import hmac

# Cripto-6.1.0
def generateSHA256Hash(data):
    """
    Generate SHA256 hash.

    Args:
        data (bytes): stream of bytes
    Returns:
        hash (SHA256) of the input data (hex).
    """
    sha256Hash = SHA256.new()
    if not isinstance(data, bytes):      # @Jan/2021 Added - compatibility with older Python2 code
        data = data.encode("utf8")
    sha256Hash.update(data)
    return sha256Hash.hexdigest()

# Cripto-6.2.0
def verifySHA256Hash(data, sha256Hash):
    """
    Verifies the SHA256 hash.

    Args:
        data (str): stream of bytes
        sha256Hash (hex): hash (SHA256) of data, to be verified
    Returns:
        True if SHA256(data) == sha256Hash; False otherwise.
    """
    return (generateSHA256Hash(data) == sha256Hash)

# Cripto-6.3.0
def generateHMAC(data, secret):
    """
    Generate HMAC-SHA256. The keyed-hash message authentication code (HMAC) is
    a specific type of message authentication code (MAC) involving a cryptographic hash
    function (SHA256) in combination with a secret key. As with any MAC, it may be
    used to simultaneously verify both the data integrity and the authentication of
    a message.

    Args:
        data (bytes): stream of bytes
        secret (bytes): secret key 
    Returns:
        HMAC-SHA256 of the input data (hex).
    """
    if not isinstance(data, bytes):   # @Jan/2021 Added - compatibility with older Python2 code
        data = data.encode("utf8")
    if not isinstance(secret, bytes):  # @Jan/2021 Added - compatibility with older Python2 code
        secret = secret.encode("utf8")
    hmacSHA256 = hmac.new(secret, msg=data, digestmod=SHA256)
    return hmacSHA256.hexdigest()

# Cripto-6.3.2
def verifyHMAC(data, hmacHash, secret):
    """
    Verifies the HMAC-SHA256.

    Args:
        data (bytes): stream of bytes
        hmacHash (hex): HMAC-SHA256 of data, to be verified
        secret (bytes): secret key used to generate hmacHash
    Returns:
        True if HMAC-SHA256(data, secret) == hmacHash; False otherwise.
    """
    return (generateHMAC(data, secret) == hmacHash)
