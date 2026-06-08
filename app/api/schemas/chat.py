from pydantic import BaseModel, Field

class ChatQueryRequest(BaseModel):
    query:str = Field(
        ...,
        min_length=1,
        description="User question to answer using the RAG pipeline."

    )

class SourceResponse(BaseModel):
    """Source metadata returned with the generated answer"""
    source_file:str|None =None
    page:int|None = None
    score:float|None = None
    preview:str|None = None


class ChatQueryResponse(BaseModel):
    """Response body returned by the RAG pipeline"""
    query:str
    answer:str
    sources:list[SourceResponse]