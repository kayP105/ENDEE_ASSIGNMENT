import subprocess


def generate_answer(question, contexts):
    MAX_CHARS = 800

    context_text = "\n\n".join(
        f"(Source: {c['meta']['source']}, Page {c['meta']['page']})\n"
        f"{c['meta']['text'][:MAX_CHARS]}"
        for c in contexts
    )


    prompt = f"""
You are a helpful assistant.
Answer the question ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context_text}

Question:
{question}

Answer:
"""
    prompt_bytes = prompt.encode("utf-8")

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode("utf-8", errors="ignore").strip()

