import random
import string
from models.url_map import URLMap


def generate_short_code(length=6):
    """
    Combination of 6 random alphanumerical characters to generate unique short url code.
    """
    characters = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(characters, k=length))
        if not URLMap.query.get(code):
            return code
