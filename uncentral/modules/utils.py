#
# modules/utils.py
#

import os
import string
import random
import shutil


def gen_random_alpha(length: int = 10):
    """Generate a random alphanumeric string.
    
    """    
    # A-Z, a-z, 0-9
    chars = string.ascii_letters + string.digits

    return ''.join(random.choice(chars) for _ in range(length))


def gen_tmp_filename(filepath: str):
    """Generate a temporary string for a filepath.
    
    """
    
    # Extract the filename from a file path.
    filename = os.path.basename(filepath)

    random_alpha = gen_random_alpha()

    tmp_filename_string = f'temp_{filename}_{random_alpha}'

    return tmp_filename_string


def move_file(src, dst):    
    if os.path.exists(dst):
        # Split the destination file into name and extension
        base, extension = os.path.splitext(dst)
        counter = 1
        
        # Create a new filename by appending a number
        while os.path.exists(dst):
            dst = f'{base}_{counter}{extension}'
            counter += 1

    # Move the file
    shutil.move(src, dst)