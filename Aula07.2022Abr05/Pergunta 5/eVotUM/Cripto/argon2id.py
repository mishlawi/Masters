# coding: latin-1

###############################################################################
# eVotUM - Electronic Voting System
#
# argon2id.py
#
# Cripto-8.0.0 - ARGON2ID
#
# Copyright (c) 2021 Universidade do Minho
# Developed by José Miranda - Devise Futures, Lda. (jose.miranda@devisefutures.com)
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
Argon2 is a key derivation function that was selected as the winner of the Password Hashing Competition 
in July 2015, and provides three related versions:
+ Argon2d maximizes resistance to GPU cracking attacks. It accesses the memory array in a password dependent order, 
which reduces the possibility of time–memory trade-off (TMTO) attacks, but introduces possible side-channel attacks.
+ Argon2i is optimized to resist side-channel attacks. It accesses the memory array in a password independent order.
+ Argon2id is a hybrid version. It follows the Argon2i approach for the first half pass over memory and the Argon2d 
approach for subsequent passes. The Internet draft https://tools.ietf.org/html/draft-irtf-cfrg-argon2-12 recommends 
using Argon2id except when there are reasons to prefer one of the other two modes.

"""

import argon2

KDF_SALT_BYTES_LENGTH = 32
KDF_HASH_LENGTH = 32
KDF_N_ITERATIONS = 100
KDF_PARALLELISM = 16
KDF_MEMORY_COST = 10240  # Memory requirements in kibibytes


# Cripto-8.1.0
def generateARGON2ID(password):
    """
    Generate derived Key.

    Args:
        password (str): password or passphrase
    Returns:
        derivedKey (hex): hex with derived Key (includes salt)
    """
    ph = argon2.PasswordHasher(time_cost=KDF_N_ITERATIONS, hash_len=KDF_HASH_LENGTH,
                               salt_len=KDF_SALT_BYTES_LENGTH, parallelism=KDF_PARALLELISM, memory_cost=KDF_MEMORY_COST)
    derivedKey = ph.hash(password)
    return bytes(derivedKey, 'utf8').hex()

# Cripto-8.2.0


def verifyARGON2ID(password, derivedKey):
    """
    Validate password.

    Args:
        password (str): password or passphrase to be validated
        derivedKey (hex): result of generateARGON2ID(password)
    Returns:
        True if password matches derivedKey; False otherwise
    """
    ph = argon2.PasswordHasher(time_cost=KDF_N_ITERATIONS, hash_len=KDF_HASH_LENGTH,
                               salt_len=KDF_SALT_BYTES_LENGTH, parallelism=KDF_PARALLELISM, memory_cost=KDF_MEMORY_COST)
    try:
        ph.verify(bytes.fromhex(derivedKey), password)
    except:
        return False
    return True
