import string


def remove_punctuation(text):
    if not text:
        return text
    return ''.join(ch for ch in text if ch not in string.punctuation)


