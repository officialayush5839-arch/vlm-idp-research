"""Centralized Prompt Management and Cryptographic Hash Tracking."""

import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple


class PromptManager:
    """Manages frozen prompt templates and guarantees cryptographic versioning."""

    def __init__(self, prompt_dir: str = "configs/phase2/prompts"):
        self.prompt_dir = Path(prompt_dir)
        self._cache: Dict[str, Tuple[str, str]] = {}

    def load_prompt_template(self, prompt_file: str) -> Tuple[str, str]:
        """Load template text and compute its SHA-256 fingerprint."""
        if prompt_file in self._cache:
            return self._cache[prompt_file]

        path = Path(prompt_file)
        if not path.is_absolute():
            path = self.prompt_dir / path.name

        if not path.exists():
            raise FileNotFoundError(f"Prompt template file not found: {path}")

        template_text = path.read_text(encoding="utf-8").strip()
        template_hash = hashlib.sha256(template_text.encode("utf-8")).hexdigest()[:16]
        self._cache[prompt_file] = (template_text, template_hash)
        return template_text, template_hash

    def format_prompt(
        self,
        prompt_file: str,
        version_tag: str,
        **kwargs: Any
    ) -> Tuple[str, str, str]:
        """
        Format prompt template with keyword arguments.
        Returns: (formatted_text, version_tag, prompt_hash)
        """
        template_text, template_hash = self.load_prompt_template(prompt_file)
        try:
            formatted_text = template_text.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required parameter for prompt template: {e}")

        return formatted_text, version_tag, template_hash
