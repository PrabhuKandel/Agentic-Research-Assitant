from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from app.config import settings



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

   
  
    # Create groq chat model for response generation
    llm = ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
        temperature=settings.llm_temperature,
    )

    # Prepare retrieved chunks as grounded context
    context = format_context(retrieved_documents)

    # Create a prompt template for the LLM
    # Keep the prompt strict so the model answers only from retrieved context
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
               """
                    You are a strict research assistant.


                    Follow every rule exactly.

                    ANSWER RULES
                    1. Answer only from the provided context.
                    2. Do not use outside knowledge.
                    3. Do not invent facts, filenames, page numbers, or citations.
                    4. If the answer is not in the context, say exactly:
                    "I do not have enough information in the uploaded documents."
                    5. Keep the answer clear and concise.

                    SOURCE RULES
                    6. Always add a Sources section at the end.
                    7. List only sources actually used in the answer.
                    8. Group all pages from the same filename into one line.
                    9. Never repeat the same filename.
                    10. Never repeat the same page number.
                    11. Sort page numbers in ascending order.
                    12. Use "page" for one page and "pages" for multiple pages.
                    13. Use exactly this format:
                        Sources:
                        - <filename>: page <number>
                        - <filename>: pages <number>, <number>, <number>

                    CORRECT EXAMPLES

                    Example 1: same file used on multiple pages

                    Sources:
                    - Insurance_Claim_Process.pdf: pages 1, 2, 3, 4, 5

                    Example 2: multiple files

                    Sources:
                    - Insurance_Claim_Process.pdf: pages 1, 3, 4
                    - Billing_Policy.pdf: page 2
                    - Claims_Guide.pdf: pages 5, 7

                    INCORRECT EXAMPLES

                    Do not return this:

                    Sources:
                    - Insurance_Claim_Process.pdf: page 1
                    - Insurance_Claim_Process.pdf: page 3
                    - Insurance_Claim_Process.pdf: page 1

                    Do not return this:

                    Sources:
                    - Insurance_Claim_Process.pdf: pages 1, 3
                    - Insurance_Claim_Process.pdf: pages 4, 5

                    The correct grouped version is:

                    Sources:
                    - Insurance_Claim_Process.pdf: pages 1, 3, 4, 5

                    14. Do not mention chunk IDs, source numbers, or internal context formatting.
                    15. Before returning the answer, verify that each filename appears only once in the Sources section.
                    """,
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


