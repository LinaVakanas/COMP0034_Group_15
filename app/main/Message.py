# Duc Tung Le
# comment for video

class Message:
    CHAR_LIMIT = 300

    def __init__(self, writer, receiver, text, have_attachment, time_stamp):
        self.writer = writer
        self.receiver = receiver
        self.text = text
        self.have_attachment = have_attachment
        self.time_stamp = time_stamp

    def length_check(self):
        if 0 < len(self.text) <= self.CHAR_LIMIT:
            return True
        elif len(self.text) > self.CHAR_LIMIT:
            return False
        else:
            return False

    def __str__(self):
        if self.have_attachment is True:
            return "Awaiting for administration confirmation"
        else:
            return "You have no attachment in the message"
