#!/usr/bin/env python
"""
This script contains methods used to generate a pseudo-random session token
"""

import os, binascii


def generate_session_id(num_bytes = 16):
    """Generates a random session token

    Args:
        num_bytes (int, optional): Number of bytes to generate. Defaults to 16.

    Returns:
        int: session token
    """    
    return binascii.b2a_hex(os.urandom(num_bytes))