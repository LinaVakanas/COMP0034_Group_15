class User:

    def __init__(self, user_type, email, name, surname, gender,
                 is_muted=False, mute_count=0, post_history=[]):
        self._user_type = user_type
        self._email = email
        self._name = name
        self._surname = surname
        self._gender = gender
        self.is_muted = is_muted
        self.mute_count = mute_count
        self._post_history = post_history

    def view_forum(self, forum_name):
        pass

    def create_post(self, forum_name, is_anonymous):
        pass

    @staticmethod
    def report(issue):
        pass
