"""Example existing script: summarizes a text file."""


def main(input_path: str, max_words: int = 50, uppercase: bool = False) -> str:
    """Pretend this does real work (e.g. summarization)."""
    try:
        with open(input_path, "r") as f:
            text = f.read()
    except FileNotFoundError:
        return f"File not found: {input_path}"

    words = text.split()[:max_words]
    result = " ".join(words)
    if uppercase:
        result = result.upper()
    return result
