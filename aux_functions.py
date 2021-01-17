import re

def remove_characters_except_number_letter(string):
    return re.sub('[\W_]+', '', string).lower()

def get_things_split(things, sep = ','):
    return things.split(sep)
