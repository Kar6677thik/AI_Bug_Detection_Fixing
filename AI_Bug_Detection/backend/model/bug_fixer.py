from typing import List, Dict
from .bug_detection import BugDetector
import torch

class BugFixer(BugDetector):
    def __init__(self, model_name: str = "deepseek-ai/deepseek-coder-1.3b-base"):
        """Initialize bug fixer with same base model as detector"""
        super().__init__(model_name)

    def suggest_fixes(self, code: str, bug_report: Dict) -> List[Dict]:
        """
        Generate suggested fixes for detected bugs
        Args:
            code: Original source code
            bug_report: Output from bug detection
        Returns:
            List of potential fixes with confidence scores
        """
        fixes = []
        for bug in bug_report.get('bugs', []):
            prompt = self._create_fix_prompt(code, bug)
            fix = self._generate_fix(prompt)
            fixes.append({
                'bug': bug,
                'fix': fix,
                'confidence': self._calculate_confidence(fix)
            })
        return fixes

    def _create_fix_prompt(self, code: str, bug: Dict) -> str:
        """Create prompt for fix generation"""
        return f"Fix this bug in the code:\n```\n{code}\n```\nBug: {bug['description']}\nFixed Code:"

    def _generate_fix(self, prompt: str) -> str:
        """Generate fix using the model"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=400,
                temperature=0.5,
                do_sample=True
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _calculate_confidence(self, fix: str) -> float:
        """Calculate confidence score for a generated fix"""
        # Simple placeholder - would implement proper scoring
        return 0.8