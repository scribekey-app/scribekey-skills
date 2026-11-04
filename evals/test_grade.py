"""Offline regression checks for the mechanical grader."""
import unittest

from grade import CHECKS, TELLS, passed


class ProfessionalDurationTest(unittest.TestCase):
    def test_professional_4_duration_and_requirements(self):
        cases = [
            ("The supplier delayed the project by 2 weeks.", True),
            ("The SUPPLIER delayed the project by TWO WEEKS.", True),
            ("The supplier delayed the project by 12 weeks.", False),
            ("The supplier delayed the project by 3 weeks.", False),
            ("The supplier delayed the project by xtwo weeks.", False),
            ("The supplier delayed the project by 2 weeksx.", False),
        ]
        for duration in ("2 weeks", "two weeks"):
            cases.append((f"The project is delayed by {duration}.", False))
            cases.extend((f"The supplier needs {duration}. {tell}", False) for tell in TELLS)
        for output, expected in cases:
            with self.subTest(output=output):
                self.assertIs(passed("professional-4", output), expected)
                self.assertIs(CHECKS["professional-4"](output), expected)


if __name__ == "__main__":
    unittest.main()
