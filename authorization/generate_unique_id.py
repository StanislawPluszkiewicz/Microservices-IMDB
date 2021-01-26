#!/usr/bin/env python
"""
This script contains methods used to generate a pseudo-random session token
"""

# uuid is a standard python package
# pip install pyOpenSSL
import uuid, OpenSSL

def generate_session_id(num_bytes = 16):
    """Generates a random session token

    Args:
        num_bytes (int, optional): Number of bytes to generate. Defaults to 16.

    Returns:
        int: session token
    """    
    return uuid.UUID(OpenSSL.rand.bytes(num_bytes))