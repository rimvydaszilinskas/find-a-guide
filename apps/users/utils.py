import os
import string
import random


def profile_picture_upload_util(instance, filename):
    upload_to = 'org'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.slug, ext)

    return os.path.join(upload_to, filename)


def generate_verification_string():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(50)])
