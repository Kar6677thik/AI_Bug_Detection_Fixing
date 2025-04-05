import unittest
from backend.model.bug_detection import BugDetector
from backend.model.bug_fixer import BugFixer

class TestBugDetection(unittest.TestCase):
    def setUp(self):
        self.detector = BugDetector()
        self.fixer = BugFixer()

    def test_bug_detection(self):
        code_with_bug = "def faulty_function():\n    return 1 / 0"  # Division by zero
        result = self.detector.detect_bugs(code_with_bug)
        self.assertTrue(len(result['bugs']) > 0, "Should detect at least one bug")

    def test_fix_suggestion(self):
        code_with_bug = "def faulty_function():\n    return 1 / 0"  # Division by zero
        bug_report = self.detector.detect_bugs(code_with_bug)
        fixes = self.fixer.suggest_fixes(code_with_bug, bug_report)
        self.assertTrue(len(fixes) > 0, "Should suggest at least one fix")

if __name__ == '__main__':
    unittest.main()