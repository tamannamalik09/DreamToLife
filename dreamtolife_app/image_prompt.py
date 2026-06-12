"""
Mock AI Image Prompt Generator: creates descriptive image prompts from
dream text. This is a textual prompt only and does not call any image API.
"""

class ImagePromptGenerator:
    def generate(self, text: str) -> str:
        t = text.strip()
        # Keep prompt concise and descriptive
        prompt = f"A surreal, cinematic scene inspired by this dream: {t[:200]}"
        prompt += ". Emphasize mood, color palette, central symbol, and emotional atmosphere."
        return prompt
