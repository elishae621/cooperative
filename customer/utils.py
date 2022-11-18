import random
import uuid


def generate_filename():
    return str(uuid.uuid4())[-3:].upper() + '-' + str(random.randint(1, 1000))
