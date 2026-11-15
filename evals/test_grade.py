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


class CleanPodcastTest(unittest.TestCase):
    def test_an_ad_leaves_no_marker(self):
        kept = "**Speaker 1:** The trial ran in 12 schools across Leeds.\n\n**Speaker 1:** The reading scores went up by 9 points."
        self.assertTrue(passed("clean-podcast-1", kept))
        self.assertFalse(passed("clean-podcast-1", kept.replace("\n\n", "\n\n[Sponsor segment removed]\n\n", 1)))


class FlowchartShapeTest(unittest.TestCase):
    def test_one_chart_with_pills_only_at_its_ends(self):
        from grade import diagram_checks
        good = 'flowchart TD\n    n1(["Log the request"]) --> n2["Approve it"]\n    n2 --> n3(["Pay it"])'
        self.assertTrue(diagram_checks("flowchart-8", good)["shapes"])
        self.assertFalse(diagram_checks("flowchart-8", good.replace('n2["Approve it"]', 'n2(["Approve it"])'))["shapes"])
        self.assertFalse(diagram_checks("flowchart-8", good + '\n    n4(["Ask for an update"]) --> n5(["Reply"])')["shapes"])


class ConversationNotesTest(unittest.TestCase):
    def test_one_on_one_preserves_action_owners(self):
        good = "### Ellis\n**Updates**\n- Shipped the reimbursement flow\n**Blockers**\n- Audit approval\n### Feedback\n- Noor to Ellis: the audit notes were unusually clear\n### Actions\n- [ ] Ellis: patch the receipt error by Thursday\n- [ ] Noor: chase the approval by Tuesday"
        self.assertTrue(passed("meeting-notes-11", good))
        self.assertFalse(passed("meeting-notes-11", good.replace("Ellis:", "Other:").replace("Noor:", "Ellis:").replace("Other:", "Noor:")))

    def test_actions_preset_rejects_extra_sections(self):
        good = "### Actions\n#### Zara\n- [ ] Send the invoice by Monday\n\n#### Ivo\n- [ ] Book the courier for Wednesday"
        self.assertTrue(passed("meeting-notes-12", good))
        self.assertFalse(passed("meeting-notes-12", good.replace("Zara", "Other").replace("Ivo", "Zara").replace("Other", "Ivo")))
        self.assertFalse(passed("meeting-notes-12", good + "\n### Decisions\n- Use green labels"))

    def test_disabled_actions_cannot_leak_into_updates(self):
        good = "### Priya\n**Updates**\nFinished the alert dashboard.\n### Feedback\nLeo to Priya: the incident report omitted the root cause and delayed the handover."
        self.assertTrue(passed("meeting-notes-13", good))
        self.assertFalse(passed("meeting-notes-13", good + "\nLeo will rotate the certificate by Friday."))


class CardShapeTest(unittest.TestCase):
    def test_a_card_is_one_question_and_one_answer(self):
        card = "**Q:** When was the Treaty of Waitangi signed?\n\n**A:** 1840."
        self.assertTrue(passed("flashcards-2", card))
        self.assertFalse(passed("flashcards-2", card.replace("\n\n**A:** ", " :: ")))
        self.assertFalse(passed("flashcards-2", "## Waitangi\n" + card))

    def test_one_idea_is_one_bold_led_bullet(self):
        self.assertTrue(passed("takeaways-2", "- **Write the test before you fix the bug.**"))
        self.assertFalse(passed("takeaways-2", "Write the test before you fix the bug."))


if __name__ == "__main__":
    unittest.main()
