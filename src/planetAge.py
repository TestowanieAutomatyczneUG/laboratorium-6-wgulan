class PlanetAge:
    def calculate_age(self, planet, age_in_sec):
        """ Calculate age on planet
        >>> pAge = PlanetAge()
        >>> pAge.calculate_age("Ziemia", 1000000000)
        31.69
        >>> pAge.calculate_age("Merkury", 2000000000)
        263.14
        >>> pAge.calculate_age("Wenus", 3000000000)
        154.53
        >>> pAge.calculate_age("Mars", 4000000000)
        67.39
        >>> pAge.calculate_age("Jowisz", 100000000)
        0.27
        >>> pAge.calculate_age("Saturn", 2000000000)
        2.15
        >>> pAge.calculate_age("Uran", 3000000000)
        1.13
        >>> pAge.calculate_age("Neptun", 4000000000)
        0.77
        >>> pAge.calculate_age("Planeta", 100000)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        Exception: Error
        >>> pAge.calculate_age(10000, -1000)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        Exception: Error
        >>> pAge.calculate_age("Ziemia", -100)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        Exception: Error
        >>> pAge.calculate_age(None, -1000)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        Exception: Error
        >>> pAge.calculate_age("Wenus", None)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        Exception: Error
        >>> pAge.calculate_age(None, None)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        Exception: Error
        """
        earth_age = 31557600
        planets = {
            "Ziemia": 1,
            "Merkury": 0.2408467,
            "Wenus": 0.61519726,
            "Mars": 1.8808158,
            "Jowisz": 11.862615,
            "Saturn": 29.447498,
            "Uran": 84.016846,
            "Neptun": 164.79132
        }

        if type(age_in_sec) == int and type(planet) == str:
            if planet in planets and age_in_sec > 0:
                age = age_in_sec / planets[planet] / earth_age
                return round(age, 2)
            else:
                raise Exception("Error")
        else:
            raise Exception("Error")



if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'pAge': PlanetAge()})