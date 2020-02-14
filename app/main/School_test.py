# Unit test
# By Khishignuur Batbold
# "py -m pip install validate_email" required

import unittest
from School import School
from validate_email import validate_email


class TestSchool(unittest.TestCase):

    def setUp(self):
        self.school = School("Smith", "email@school.com", "password123", "school_info")

    def test_name(self):
        self.assertTrue(self.school._name.isalnum())

    def test_email(self):
        self.assertTrue(validate_email(self.school._email))

    def test_password(self):
        self.assertTrue(self.school._password.isalnum())
