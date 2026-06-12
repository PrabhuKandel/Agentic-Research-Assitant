from app.models.document import Document, DocumentChunk

# Allows: from app.models import Document, DocumentChunk instead of importing from app.models.document.
__all__ = ["Document", "DocumentChunk"]