## Mahdi Shah

class Reply:

    CHAR_LIMIT = 280

    def __init__(self, author, text, is_anonymous, parent_title, parent_author):
        self.author = author
        self._text = text
        self._is_anonymous = is_anonymous
        self._parent_title = parent_title
        self.parent_author = parent_author ## Mahdi Shah

    def __str__(self):
        if self._is_anonymous is False:
            return "{} is replying to {}\n".format(self.author, self.parent_author)
        else:
            return "Anonymous is replying to {}\n".format(self.parent_author)

    def check_length(self):
        if 0 < len(self._text) <= self.CHAR_LIMIT:
            return True
        elif len(self._text) > self.CHAR_LIMIT:
            return False
        else:
            return False
