agentic-research-assistant/
│
├── app/
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   ├── upload.py
│   │   │   └── query.py
│   │   │
│   │   └── schemas/
│   │       ├── upload.py
│   │       └── query.py
│   │
│   ├── services/
│   │   ├── document_loader.py
│   │   ├── text_preprocessor.py
│   │   ├── chunker.py
│   │   ├── embedding_service.py
│   │   ├── vector_store.py
│   │   ├── retrieval_service.py
│   │   └── generation_service.py
│   │
│   ├── models/
│   │   ├── document.py
│   │   └── chunk.py
│   │
│   ├── utils/
│   │   ├── file_validation.py
│   │   ├── logging.py
│   │   └── errors.py
│   │
│   ├── prompts/
│   │   └── rag_answer_prompt.txt
│   │
│   ├── config.py
│   ├── dependencies.py
│   └── main.py
│
├── data/
│   ├── uploads/
│   ├── processed/
│   └── vector_db/
│
├── tests/
│   ├── test_file_validation.py
│   ├── test_document_loader.py
│   ├── test_chunker.py
│   └── test_retrieval.py
│
├── docs/
│   ├── architecture.md
│   ├── ingestion_pipeline.md
│   └── rag_flow.md
│
├── frontend/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml