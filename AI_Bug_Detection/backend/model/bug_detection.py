import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List, Dict
import numpy as np
import os

class BugDetector:
    def __init__(self, model_name: str = "deepseek-ai/deepseek-coder-1.3b-base"):
        """Initialize the bug detection model with quantization for low-end machines"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Create an offload folder if it doesn't exist
        offload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_offload")
        os.makedirs(offload_dir, exist_ok=True)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            device_map="auto",
            offload_folder=offload_dir  # Add offload folder
        )
        self.model.eval()

    def detect_bugs(self, code: str) -> Dict:
        """
        Analyze code and return detected bugs with confidence scores
        Args:
            code: Input source code to analyze
        Returns:
            Dictionary containing detected bugs and metadata
        """
        inputs = self.tokenizer(
            f"Analyze this code for bugs:\n```\n{code}\n```\nBugs:",
            return_tensors="pt",
            truncation=True,
            max_length=2048
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.7,
                do_sample=True
            )
        
        analysis = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._parse_analysis(analysis)

    def _parse_analysis(self, raw_output: str) -> Dict:
        """Parse model output into structured bug report"""
        # Implementation would parse the raw text output into structured format
        return {
            "bugs": [],
            "warnings": [],
            "analysis": raw_output
        }