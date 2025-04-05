import re
from typing import List, Dict
import tokenize
import io

class CodePreprocessor:
    def __init__(self):
        """Initialize code preprocessing utilities"""
        self.language_handlers = {
            'python': self._preprocess_python,
            'javascript': self._preprocess_javascript,
            'default': self._preprocess_generic
        }   
        
    def preprocess(self, code: str, language: str = 'python') -> Dict:
        """
        Preprocess code for analysis
        Args:
            code: Source code to preprocess
            language: Programming language of the code
        Returns:
            Dictionary containing processed code and metadata
        """
        handler = self.language_handlers.get(language.lower(), self.language_handlers['default'])
        return handler(code)
        
    def _preprocess_python(self, code: str) -> Dict:
        """Python-specific preprocessing"""
        # Remove comments and docstrings
        cleaned_code = self._remove_comments_and_docstrings(code)
        # Normalize whitespace
        cleaned_code = '\n'.join(line.strip() for line in cleaned_code.split('\n') if line.strip())
        return {
            'processed_code': cleaned_code,
            'language': 'python',
            'tokens': self._tokenize_python(cleaned_code)
        }
        
    def _preprocess_javascript(self, code: str) -> Dict:
        """JavaScript-specific preprocessing"""
        # Remove comments
        cleaned_code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.DOTALL)
        # Normalize whitespace
        cleaned_code = '\n'.join(line.strip() for line in cleaned_code.split('\n') if line.strip())
        return {
            'processed_code': cleaned_code,
            'language': 'javascript',
            'tokens': cleaned_code.split()
        }
        
    def _preprocess_generic(self, code: str) -> Dict:
        """Generic preprocessing for other languages"""
        # Basic cleaning for unknown languages
        cleaned_code = '\n'.join(line.strip() for line in code.split('\n') if line.strip())
        return {
            'processed_code': cleaned_code,
            'language': 'unknown',
            'tokens': cleaned_code.split()
        }
        
    def _remove_comments_and_docstrings(self, source: str) -> str:
        """Remove Python comments and docstrings while preserving other content"""
        io_obj = io.StringIO(source)
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
                
            if token_type == tokenize.COMMENT:
                pass
            elif token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
                    if prev_toktype != tokenize.NEWLINE:
                        if start_col > 0:
                            out += token_string
                else:
                    out += token_string
                    
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line
            
        return out
        
    def _tokenize_python(self, code: str) -> List[str]:
        """Tokenize Python code while preserving structure"""
        try:
            tokens = []
            io_obj = io.StringIO(code)
            for tok in tokenize.generate_tokens(io_obj.readline):
                if tok.type != tokenize.ENDMARKER:
                    tokens.append(tok.string)
            return tokens
        except:
            return code.split()