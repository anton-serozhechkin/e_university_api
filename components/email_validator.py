import re   


def validate_email(email):
    """
    The method is using for email validation. Only letters (a-z), numbers (0-9) and periods (.) are allowed
    :return: True or not None string
    """
    specials = '!#$%&\'*+-/=?^_`{|?.'
    specials = re.escape(specials)
    regex = re.compile('^(?![' + specials + '])'
                       '(?!.*[' + specials + ']{2})'
                       '(?!.*[' + specials + ']$)'
                       '[A-Za-z0-9' + specials + ']+(?<!['+ specials + '])@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')
    message = False
    if not email:
        message = "Електронний адрес не може бути порожнім"
    if not re.fullmatch(regex, email):
        message = f"Невірний формат адресу електронної пошти: {email}."
    if message:
        raise ValueError(message)
    return True
