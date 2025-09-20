from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from transformers import pipeline
from langchain.chains import RetrievalQA
from huggingface_hub import login
from dotenv import load_dotenv
from config import settings
from system_prompt import system_prompt

login(settings.huggingface_token)

def docs_to_text(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def model(retriever):
    pipe = pipeline("text2text-generation", model=settings.huggingface_chat_model, max_new_tokens=150)
    llm = HuggingFacePipeline(pipeline=pipe)
    PROMPT = PromptTemplate(
        template=system_prompt, input_variables=["context", "question"]
        )
    document_chain = create_stuff_documents_chain(llm=llm, prompt=PROMPT)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain

    