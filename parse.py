from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content:\n\n"
    "{dom_content}\n\n"
    "Instructions:\n"
    "1. Extract ONLY what matches: {parse_description}\n"
    "2. No extra text or explanation.\n"
    "3. If nothing matches, return an empty string ('')."
)

model = OllamaLLM(model="llama3.2")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({
            "dom_content": chunk,
            "parse_description": parse_description
        })
        print(f"Parsed chunk {i}/{len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
