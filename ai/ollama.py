from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def ollama_reasoning(title, category, estimate, importance, energy, due):
    template = """
    Task: {title}
    Category: {category}
    Estimated duration: {estimate} minutes
    Importance: {importance}/5
    Energy level: {energy}/5
    Due date: {due}

    In 1–2 short sentences, explain how the user should prioritize this task.
    Be concise and practical.
    """

    # Make due date display nicely if it's None/empty
    due_text = due if due else "None"

    model = OllamaLLM(model="llama3", temperature=0.3)
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | model

    # Invoke the chain with variables, then return plain text
    result = chain.invoke({
        "title": title,
        "category": category,
        "estimate": estimate,
        "importance": importance,
        "energy": energy,
        "due": due_text
    })

    return str(result).strip()
