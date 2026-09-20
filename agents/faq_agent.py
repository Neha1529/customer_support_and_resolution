from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI


_FAQ_PATH = Path("D:\projects\customer_support_and_resolution\faq.md")

_faq_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a customer support assistant. Answer the customer's "
            "question using ONLY the FAQ document below. If the answer "
            "isn't in the document, say you don't know.\n\n"
            "FAQ document:\n{faq_text}",
        ),
        ("human", "{question}"),
    ]
)
_faq_llm = ChatVertexAI(model="gemini-2.5-flash", temperature=0)
_faq_chain = _faq_prompt | _faq_llm


def answer_faq_question(question: str) -> str:
    """Answer a customer's FAQ/policy question from the FAQ document."""
    faq_text = _FAQ_PATH.read_text()
    result = _faq_chain.invoke({"faq_text": faq_text, "question": question})
    return result.content