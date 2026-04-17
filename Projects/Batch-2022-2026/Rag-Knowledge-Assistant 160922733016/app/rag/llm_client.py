from typing import List, Dict
import ollama

def generate_answer(question: str, chunks: List[Dict], **kwargs) -> str:

    context_parts = []
    for chunk in chunks:
        source = chunk.get("source_file", "unknown")
        text = chunk.get("text_chunk", "")
        context_parts.append(f"[Source: {source}]\n{text}")

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
Answer the question ONLY using the context.

If the answer is not in the context say:
"I could not find the answer in the product documentation."

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]