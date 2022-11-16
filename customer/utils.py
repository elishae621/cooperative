import random
import uuid

def generate_slug(self):
    return "G" + self.id

def generate_filename():
    return str(uuid.uuid4())[-3:].upper() + '-' + str(random.randint(1, 1000))
