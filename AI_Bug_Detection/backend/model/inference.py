from .bug_detection import BugDetector
from .bug_fixer import BugFixer

class InferenceEngine:
    def __init__(self):
        """Initialize the inference engine with bug detection and fixing capabilities"""
        self.detector = BugDetector()
        self.fixer = BugFixer()
        
    def analyze_code(self, code: str) -> dict:
        """
        Analyze the provided code for bugs and suggest fixes
        Args:
            code: Source code to analyze
        Returns:
            Dictionary containing bug analysis and suggested fixes
        """
        bug_report = self.detector.detect_bugs(code)
        fixes = self.fixer.suggest_fixes(code, bug_report)
        return {
            'bug_report': bug_report,
            'fixes': fixes
        }