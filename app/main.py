from fastapi import FastAPI

app = FastAPI(

    title="Agentic Research Assistant API",
    description="API for ingesting documents and querying the agentic research assistant.",
    version="1.0.0",
)

@app.get("/")
def health_check()->dict[str, str]:
    return {
        "status": "ok", 
        "message": "Agentic Research Assistant API is running."
        }