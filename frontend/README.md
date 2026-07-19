# Agentic Research Assistant Frontend

A Next.js + TypeScript + Tailwind CSS frontend for the FastAPI Agentic Research Assistant backend.

## Run locally

1. Copy the environment file:

```bash
cp .env.example .env.local
```

On Windows you can create `.env.local` manually and add:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

2. Install dependencies:

```bash
npm install
```

3. Start the frontend:

```bash
npm run dev
```

4. Open:

```text
http://localhost:3000
```

Your FastAPI backend must be running at `http://localhost:8000`, with CORS enabled for `http://localhost:3000`.

## Pages

- `/` — welcome page and create-new-chat action
- `/chats/[chatId]` — chat history and message composer
- `/documents` — upload, list, and delete knowledge-base documents

## Backend APIs used

### Chats

- `POST /chats` — create a chat
- `GET /chats` — load recent chats
- `GET /chats/{chat_id}` — load one chat and its messages
- `POST /chats/{chat_id}/messages` — send a message and receive the assistant answer
- `DELETE /chats/{chat_id}` — delete a chat

### Documents

- `POST /documents/upload` — upload and ingest a file using multipart form field `file`
- `GET /documents` — list uploaded documents
- `DELETE /documents/{document_id}` — delete a document and stored chunks

## Static parts

- Product name: `Research Assistant`
- Welcome text and helper messages
- Supported-file text: PDF and TXT
- Sidebar labels and page titles
- Colors and layout

## Dynamic parts

- Recent chats
- Chat title and message history
- Assistant answers
- Uploaded document list
- Document status and dates
- Upload/delete success and error messages

## MVP limitations

- Sources returned by the chat API are intentionally not displayed.
- No streaming response; a `Thinking...` indicator is shown until the full answer arrives.
- No rename-chat endpoint is currently available.
- No real upload percentage is available because the backend responds after ingestion completes.
- Document size is not displayed because the backend response does not include it.
- The frontend currently allows PDF and TXT selection. Update the input `accept` value only after the backend supports more formats.
