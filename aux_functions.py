import re

def remove_characters_except_number_letter(string):
    return re.sub('[\W_]+', '', string)

def get_people_split(people, sep = ','):
    return people.split(sep)
