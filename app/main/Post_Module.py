# Lina Vakanas
#hello
from Reply_Module import Reply


class Post:

    def __init__(self, author, title, text, is_anonymous=False):
        self.author = author
        self._title = title
        self._text = text
        self._is_anonymous = is_anonymous

    def __str__(self):

        if self._is_anonymous is False:
            return "author is: {} \ntitle is: {}\n".format(self.author, self._title)
        else:
            return "author is: Anonymous, title is: {}\n".format(self._title, self._is_anonymous)

    def deleted_post(self):
        pass

    def create_reply(self, reply_author, reply_text, reply_anonymous):
        if self._is_anonymous is False:
            parent_author = self.author
        else:
            parent_author = "Anonymous"
        parent_title = self._title
        if reply_anonymous == "Y":
            is_reply_anonymous = True
        else:
            is_reply_anonymous = False

        reply = Reply(reply_author, reply_text, is_reply_anonymous, parent_title, parent_author)
        # print(reply.__str__())
        return reply
