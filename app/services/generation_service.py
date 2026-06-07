import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from app.config import config



def format_context(retrieved_documents: list[Document]) -> str:
    # Combine retrieved chunks into one context block for the LLM
    context_parts = []

    for index, document in enumerate(retrieved_documents, start=1):
        source_file = document.metadata.get("source_file", "Unknown source")
        page = document.metadata.get("page", "Unknown page")

        context_parts.append(
            f"[Source {index} | File: {source_file} | Page: {page}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context_parts)


def generate_response(
    query: str, retrieved_documents: list[Document]
) -> str:

    # Load environment variables from .env file
    load_dotenv()

    # Create groq chat model for response generation
    llm = ChatGroq(
        model=config.llm_model,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=config.temperature,
    )

    # Prepare retrieved chunks as grounded context
    context = format_context(retrieved_documents)

    # Create a prompt template for the LLM
    # Keep the prompt strict so the model answers only from retrieved context
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful research assistant. Answer the user using only the provided context."
                "If the answer is not in the context, say you do not have enough information.",
            ),
            ("user", "Question:\n{question}\n\nContext:\n{context}\n\nAnswer:"),
        ]
    )

    chain = prompt_template | llm

    # Generate the response using the LLM
    response = chain.invoke(
        {
            "question": query,
            "context": context,
        }
    )

    return response.content


