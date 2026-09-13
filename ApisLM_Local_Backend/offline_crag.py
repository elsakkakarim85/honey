import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# State Definition
class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[Document]
    relevance_score: str

# 1. Initialize Zero-Cost Local LLM directly from our exported GGUF
# This guarantees NO cloud APIs (OpenAI/Anthropic) are utilized.
gguf_model_path = "../ApisLM_Local_AI/ApisLM-3B-Mobile.gguf"

print("Loading local ApisLM GGUF model via llama.cpp...")
# Note: For production execution, ensure the GGUF file exists at the path.
local_llm = LlamaCpp(
    model_path=gguf_model_path if os.path.exists(gguf_model_path) else "dummy_path_for_syntax_check.gguf",
    temperature=0.1,
    max_tokens=512,
    n_ctx=2048,
    top_p=0.9,
    verbose=False
)

def retrieve(state: GraphState):
    """Simulated local retrieval from Qdrant."""
    print("-> Retrieving from local Qdrant...")
    return {"documents": [Document(page_content="Varroa mites are treated with Oxalic Acid.")]}

def grade_documents(state: GraphState):
    """Local LLM grading if document is relevant to the question."""
    print("-> Grading relevance locally...")
    prompt = PromptTemplate.from_template("Is this document relevant to the question? Question: {question} Doc: {doc}\nAnswer yes or no.")
    chain = prompt | local_llm
    # Simulated execution
    return {"relevance_score": "yes"}

def generate(state: GraphState):
    """Local GGUF Generation."""
    print("-> Generating final answer via local ApisLM-3B-Mobile.gguf...")
    prompt = PromptTemplate.from_template("Answer based on context: {context}\nQuestion: {question}\nAnswer:")
    chain = prompt | local_llm
    # Simulated execution
    return {"generation": "Offline generation: Apply Oxalic Acid."}

def rewrite(state: GraphState):
    """Local GGUF Rewriting for better retrieval queries."""
    print("-> Rewriting query locally...")
    prompt = PromptTemplate.from_template("Rewrite this question to be better: {question}\nRewritten:")
    chain = prompt | local_llm
    # Simulated execution
    return {"question": "Rewritten local query"}

def decide_to_generate(state: GraphState):
    if state["relevance_score"] == "yes":
        return "generate"
    else:
        return "rewrite"

# Scaffold LangGraph
workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("rewrite", rewrite)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges("grade_documents", decide_to_generate)
workflow.add_edge("rewrite", "retrieve")
workflow.add_edge("generate", END)

crag_app = workflow.compile()

if __name__ == "__main__":
    print("CRAG Local Pipeline Initialized Successfully.")
    # crag_app.invoke({"question": "How to treat varroa?"})
