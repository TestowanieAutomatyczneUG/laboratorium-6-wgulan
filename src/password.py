import unittest


class Password:
    def ValidPassword(self, password):
        """
        >>> password = Password()
        >>> password.ValidPassword("R#sdgf12$")
        True
        >>> password.ValidPassword("#$%p23Cz")
        True
        >>> password.ValidPassword("abcd")
        False
        >>> password.ValidPassword("abcDefgh")
        False
        >>> password.ValidPassword("abcd1234")
        False
        >>> password.ValidPassword("ab#cdEF")
        False
        >>> password.ValidPassword("!@#$%^&*")
        False
        >>> password.ValidPassword("abcd#$%@")
        False
        >>> password.ValidPassword("")
        False
        >>> password.ValidPassword(1234)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        TypeError: Password must be a string.
        >>> password.ValidPassword(True)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        TypeError: Password must be a string.
        >>> password.ValidPassword("TRS!@$#  123")
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        ValueError: Password cannot contain spaces.
        """
        if not isinstance(password, str):
            raise TypeError("Password must be a string.")
        if any(char.isspace() for char in password):
            raise ValueError("Password cannot contain spaces.")
        if len(password) < 8:  # długosc mniejsza od 8
            return False
        if not any(char.isupper() for char in password):  # brak wielkiej litery
            return False
        if not any(char.isdigit() for char in password):  # brak cyfry
            return False
        if not any(char in "[@_!#$%^&*()<>?/|}{~:]" for char in password):  # brak specjalnego znaku
            return False
        else:
            return True

class PasswordTest(unittest.TestCase):
    def setUp(self):
        self.temp = Password()

    def test_password_correct(self):
        self.assertEqual(True, self.temp.ValidPassword("#$%p23Cz"))

    def test_password_no_uppercase(self):
        self.assertEqual(False, self.temp.ValidPassword("#$%p3fez"))

    def test_password_too_short(self):
        self.assertEqual(False, self.temp.ValidPassword("abdcf"))

    def test_password_no_special_signs(self):
        self.assertEqual(False, self.temp.ValidPassword("AS124134as"))

    def test_password_not_a_string(self):
        with self.assertRaises(TypeError):
            self.temp.ValidPassword(1234)

    def test_password_with_space(self):
        with self.assertRaises(ValueError):
            self.temp.ValidPassword("as 12313 77%")

    def tearDown(self):
        self.temp = None

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'password': Password()})
    unittest.main()
