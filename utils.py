def qna_dict_to_string(qna: dict) -> str:
    """
    Converts a dictionary of Q&A pairs into a readable string format:
    Q: <question>
    A: <answer>
    (blank line between pairs)
    """
    lines = []
    for question, answer in qna.items():
        lines.append(f"Q: {question}\nA: {answer}\n")
    return "\n".join(lines)
