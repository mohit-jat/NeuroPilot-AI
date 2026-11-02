import gradio as gr
import requests
import os
import uuid


# Backend API URLs
CHAT_URL = "http://127.0.0.1:8000/api/v1/chat/"
MEDIA_URL = "http://127.0.0.1:8000/api/v1/media/upload"
APPROVAL_URL = "http://127.0.0.1:8000/api/v1/chat/approval"

SESSIONS_URL = "http://127.0.0.1:8000/api/v1/history/sessions"
SESSION_HISTORY_URL = "http://127.0.0.1:8000/api/v1/history/session/"
CLEAR_HISTORY_URL = "http://127.0.0.1:8000/api/v1/history/clear"

DOCUMENT_UPLOAD_URL = "http://127.0.0.1:8000/api/v1/documents/upload"
DOCUMENT_ASK_URL = "http://127.0.0.1:8000/api/v1/documents/ask-saved"


# --------------------------------------------------
# SESSION HELPERS
# --------------------------------------------------

def get_session_choices():
    try:
        response = requests.get(SESSIONS_URL, timeout=5)
        if response.status_code == 200:
            sessions = response.json().get("sessions", [])
            if sessions:
                return [(f"💬 {s['title']}", s["session_id"]) for s in sessions]
    except Exception:
        pass
    return []


def create_new_chat():
    new_thread_id = f"session-{str(uuid.uuid4())[:8]}"
    choices = get_session_choices()
    return [], "", None, "", new_thread_id, gr.update(choices=choices, value=None)


def switch_session(selected_session_id):
    if not selected_session_id:
        return [], "neuropilot-default", ""

    try:
        response = requests.get(f"{SESSION_HISTORY_URL}{selected_session_id}", timeout=10)
        if response.status_code == 200:
            chats = response.json().get("history", [])
            messages = []
            for chat in chats:
                messages.append({
                    "role": "user",
                    "content": chat["user_message"]
                })
                messages.append({
                    "role": "assistant",
                    "content": chat["ai_response"]
                })
            return messages, selected_session_id, ""
    except Exception as error:
        return [{"role": "assistant", "content": f"History Error: {error}"}], selected_session_id, ""

    return [], selected_session_id, ""


def delete_selected_chat(thread_id):
    if not thread_id:
        choices = get_session_choices()
        return [], "", None, "No chat selected to delete.", thread_id, gr.update(choices=choices)

    try:
        requests.delete(f"{SESSION_HISTORY_URL}{thread_id}", timeout=10)
    except Exception as error:
        choices = get_session_choices()
        return [], "", None, f"Delete Error: {error}", thread_id, gr.update(choices=choices)

    # Start a clean new session
    new_thread_id = f"session-{str(uuid.uuid4())[:8]}"
    choices = get_session_choices()
    return [], "", None, "Chat deleted successfully.", new_thread_id, gr.update(choices=choices, value=None)


def delete_all_history():
    try:
        requests.delete(CLEAR_HISTORY_URL, timeout=10)
    except Exception:
        pass
    new_thread_id = f"session-{str(uuid.uuid4())[:8]}"
    return [], "", None, "All history cleared.", new_thread_id, gr.update(choices=[], value=None)


# --------------------------------------------------
# 1. TEXT CHAT + IMAGE + AUDIO
# --------------------------------------------------

def chat_with_ai(message, file, history, thread_id):

    if history is None:
        history = []

    message = message.strip() if message else ""

    if not message and not file:
        choices = get_session_choices()
        return history, "", None, "Please enter a message or upload a file.", thread_id, gr.update(choices=choices, value=thread_id)

    try:

        # Image or Audio Upload
        if file:

            with open(file, "rb") as uploaded_file:

                response = requests.post(
                    MEDIA_URL,
                    files={
                        "file": (
                            os.path.basename(file),
                            uploaded_file
                        )
                    },
                    data={
                        "question": message,
                        "thread_id": thread_id
                    },
                    timeout=120
                )

            response.raise_for_status()

            result = response.json()

            user_message = f"📎 Uploaded: {os.path.basename(file)}"

            if message:
                user_message += f"\n\n💬 Question: {message}"

            ai_response = result["agent_response"]

            approval_status = ""

        # Normal Text Chat
        else:

            response = requests.post(
                CHAT_URL,
                json={
                    "message": message,
                    "input_type": "text",
                    "thread_id": thread_id
                },
                timeout=120
            )

            response.raise_for_status()

            result = response.json()

            user_message = message
            ai_response = result["response"]

            # Check approval requirement
            if result.get("approval_required"):

                approval_status = (
                    "⚠️ **Approval Required**: NeuroPilot wants to use **Web Search** (DuckDuckGo). "
                    "Please **Approve** or **Reject** below."
                )

            else:

                approval_status = ""

        # Add User Message
        history.append({
            "role": "user",
            "content": user_message
        })

        # Add AI Response
        history.append({
            "role": "assistant",
            "content": ai_response
        })

    except Exception as error:

        history.append({
            "role": "assistant",
            "content": "Error: " + str(error)
        })

        approval_status = "Request failed: " + str(error)

    # Refresh session list in sidebar so the new chat shows up immediately
    choices = get_session_choices()

    return history, "", None, approval_status, thread_id, gr.update(choices=choices, value=thread_id)


# --------------------------------------------------
# 2. HUMAN APPROVAL
# --------------------------------------------------

def handle_tool_approval(decision, thread_id, history):

    if history is None:
        history = []

    if not thread_id:
        return history, "No pending approval found."

    try:

        response = requests.post(
            APPROVAL_URL,
            json={
                "thread_id": thread_id,
                "decision": decision
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        ai_response = result["response"]

        history.append({
            "role": "assistant",
            "content": ai_response
        })

        if result.get("approval_required"):

            status = "⚠️ Another approval is required."

        elif decision == "approve":

            status = "✅ Approved. Web search executed."

        else:

            status = "❌ You rejected the Web Search request."

        return history, status

    except Exception as error:

        return history, "Approval Error: " + str(error)


def approve_tool(thread_id, history):

    return handle_tool_approval(
        "approve",
        thread_id,
        history
    )


def reject_tool(thread_id, history):

    return handle_tool_approval(
        "reject",
        thread_id,
        history
    )


# --------------------------------------------------
# 3. DOCUMENT UPLOAD
# --------------------------------------------------

def upload_document(file):

    if not file:
        return None, "Please select a PDF or TXT file to upload."

    try:

        with open(file, "rb") as document:

            response = requests.post(
                DOCUMENT_UPLOAD_URL,
                files={
                    "file": (
                        os.path.basename(file),
                        document
                    )
                },
                timeout=120
            )

        response.raise_for_status()

        result = response.json()

        document_id = result["document_id"]

        status = f"✅ Document indexed successfully! File: {result['file_name']}"

        return document_id, status

    except Exception as error:

        return None, "Upload Error: " + str(error)


# --------------------------------------------------
# 4. ASK QUESTIONS FROM SAVED DOCUMENT
# --------------------------------------------------

def ask_document(document_id, question):

    if not document_id:
        return "⚠️ Please upload and index a document first."

    if not question or not question.strip():
        return "⚠️ Please enter your question about the document."

    try:

        response = requests.post(
            DOCUMENT_ASK_URL,
            data={
                "document_id": document_id,
                "question": question
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        return result["answer"]

    except Exception as error:

        return "Error: " + str(error)


# --------------------------------------------------
# 5. CHATGPT-STYLE CUSTOM CSS
# --------------------------------------------------

css = """
:root {
    --bg-main: #212121;
    --bg-sidebar: #171717;
    --bg-card: #2f2f2f;
    --text-primary: #ececec;
    --text-muted: #b4b4b4;
    --border-subtle: #303030;
    --accent-green: #10a37f;
}

body, .gradio-container {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

#sidebar-panel {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    padding: 18px !important;
}

#header-title {
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.5px !important;
}

#chat-area {
    background-color: var(--bg-main) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25) !important;
}

#chat-input textarea {
    background-color: var(--bg-card) !important;
    color: #ffffff !important;
    border: 1px solid #424242 !important;
    border-radius: 24px !important;
    padding: 14px 20px !important;
    font-size: 15px !important;
}

#chat-input textarea:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.2) !important;
}

#send-btn {
    border-radius: 50% !important;
    width: 46px !important;
    height: 46px !important;
    min-width: 46px !important;
    background-color: var(--accent-green) !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 18px !important;
}

.accordion-upload {
    background-color: #262626 !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
}

.doc-card {
    background-color: #262626 !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    padding: 16px !important;
    margin-bottom: 16px !important;
}

footer {
    display: none !important;
}
"""


# --------------------------------------------------
# 6. MAIN INTERFACE WITH PERSISTENT SESSIONS
# --------------------------------------------------

with gr.Blocks(title="NeuroPilot AI") as app:

    # Initial session ID
    initial_thread_id = f"session-{str(uuid.uuid4())[:8]}"
    thread_id_state = gr.State(value=initial_thread_id)

    with gr.Row():

        # --------------------------------------------------
        # LEFT SIDEBAR (ChatGPT Multi-Session List)
        # --------------------------------------------------
        with gr.Column(scale=1, min_width=250, elem_id="sidebar-panel"):

            gr.Markdown(
                """
                ### 🧠 **NeuroPilot AI**
                *Multimodal Assistant*
                """,
                elem_id="header-title"
            )

            new_chat_btn = gr.Button("➕ New Chat", variant="primary")

            gr.Markdown("---")

            gr.Markdown("#### 📜 **Past Conversations**")

            # Dropdown with past conversations (click to load)
            initial_choices = get_session_choices()
            session_dropdown = gr.Dropdown(
                label="Select chat to view/continue",
                choices=initial_choices,
                value=None,
                interactive=True
            )

            # Targeted delete vs clear all
            with gr.Row():
                delete_this_btn = gr.Button("🗑️ Delete This Chat", variant="stop", size="sm")
                clear_all_btn = gr.Button("⚠️ Clear All", variant="secondary", size="sm")

            gr.Markdown("---")

            gr.Markdown(
                """
                #### ⚡ **Capabilities**
                * 💬 **Smart Text Chat**
                * 🖼️ **Image Understanding**
                * 🎙️ **Audio Transcription**
                * 📄 **Document Intelligence**
                * 🌐 **Live Web Search**
                * 👤 **Human-in-the-Loop**
                
                ---
                <small style="color: #888;">Powered by LangGraph Persistence</small>
                """
            )

        # --------------------------------------------------
        # MAIN CONVERSATION / CONTENT AREA
        # --------------------------------------------------
        with gr.Column(scale=4):

            with gr.Tabs():

                # ----------------------------------
                # TAB 1: AI CHAT (ChatGPT Style)
                # ----------------------------------
                with gr.Tab("💬 Chat"):

                    chatbot = gr.Chatbot(
                        label="",
                        height=520,
                        elem_id="chat-area",
                        placeholder="### 👋 Welcome to NeuroPilot AI\nAsk a question, upload an image, audio, or explore past conversations from the sidebar."
                    )

                    # Human Approval Banner & Controls
                    approval_status = gr.Markdown("", elem_id="approval-banner")

                    with gr.Row():
                        approve_button = gr.Button("✓ Approve Search", variant="primary", size="sm")
                        reject_button = gr.Button("✕ Reject", variant="stop", size="sm")

                    # Sleek, Collapsible File Attachment
                    with gr.Accordion("📎 Attach Image or Audio (Optional)", open=False, elem_classes=["accordion-upload"]):
                        file_input = gr.File(
                            label="",
                            file_types=["image", "audio"],
                            type="filepath",
                            height=100
                        )

                    # Bottom Prompt Input Bar
                    with gr.Row():
                        message = gr.Textbox(
                            placeholder="Message NeuroPilot or ask a question...",
                            show_label=False,
                            scale=9,
                            elem_id="chat-input",
                            autofocus=True
                        )

                        send_button = gr.Button(
                            "➤",
                            variant="primary",
                            scale=1,
                            elem_id="send-btn"
                        )

                # ----------------------------------
                # TAB 2: CHAT WITH DOCUMENTS
                # ----------------------------------
                with gr.Tab("📄 Chat with Documents"):

                    gr.Markdown(
                        """
                        ### 📄 **Document Intelligence**
                        Upload a PDF or TXT file once, and ask multiple questions using vector embeddings & semantic search.
                        """
                    )

                    document_id_state = gr.State(value=None)

                    # Step 1: Upload Card
                    with gr.Group(elem_classes=["doc-card"]):
                        gr.Markdown("#### 1️⃣ **Upload Document**")
                        document_file = gr.File(
                            label="Select PDF or TXT file",
                            file_types=[".pdf", ".txt"],
                            type="filepath"
                        )
                        upload_button = gr.Button("📥 Upload & Index Document", variant="primary")
                        upload_status = gr.Textbox(
                            label="Upload Status",
                            interactive=False,
                            placeholder="Upload status will appear here..."
                        )

                    # Step 2: Query Card
                    with gr.Group(elem_classes=["doc-card"]):
                        gr.Markdown("#### 2️⃣ **Ask Questions from Document**")
                        document_question = gr.Textbox(
                            label="",
                            placeholder="Ask any question about your indexed document..."
                        )
                        document_button = gr.Button("🔍 Ask Document ➤", variant="primary")
                        document_answer = gr.Textbox(
                            label="Answer",
                            lines=6,
                            interactive=False,
                            placeholder="AI response from document will appear here..."
                        )

    # --------------------------------------------------
    # EVENT BINDINGS
    # --------------------------------------------------

    # Send button & Enter key
    send_button.click(
        chat_with_ai,
        inputs=[message, file_input, chatbot, thread_id_state],
        outputs=[chatbot, message, file_input, approval_status, thread_id_state, session_dropdown]
    )

    message.submit(
        chat_with_ai,
        inputs=[message, file_input, chatbot, thread_id_state],
        outputs=[chatbot, message, file_input, approval_status, thread_id_state, session_dropdown]
    )

    # Switch session from dropdown (Click past chat)
    session_dropdown.change(
        switch_session,
        inputs=[session_dropdown],
        outputs=[chatbot, thread_id_state, approval_status]
    )

    # ➕ New Chat
    new_chat_btn.click(
        create_new_chat,
        inputs=[],
        outputs=[chatbot, message, file_input, approval_status, thread_id_state, session_dropdown]
    )

    # 🗑️ Delete ONLY Currently Selected Chat
    delete_this_btn.click(
        delete_selected_chat,
        inputs=[thread_id_state],
        outputs=[chatbot, message, file_input, approval_status, thread_id_state, session_dropdown]
    )

    # ⚠️ Clear ALL History
    clear_all_btn.click(
        delete_all_history,
        inputs=[],
        outputs=[chatbot, message, file_input, approval_status, thread_id_state, session_dropdown]
    )

    # Human Approval
    approve_button.click(
        approve_tool,
        inputs=[thread_id_state, chatbot],
        outputs=[chatbot, approval_status]
    )

    reject_button.click(
        reject_tool,
        inputs=[thread_id_state, chatbot],
        outputs=[chatbot, approval_status]
    )

    # Document Upload & Ask
    upload_button.click(
        upload_document,
        inputs=[document_file],
        outputs=[document_id_state, upload_status]
    )

    document_button.click(
        ask_document,
        inputs=[document_id_state, document_question],
        outputs=[document_answer]
    )

    document_question.submit(
        ask_document,
        inputs=[document_id_state, document_question],
        outputs=[document_answer]
    )


# --------------------------------------------------
# 7. LAUNCH APPLICATION
# --------------------------------------------------

app.launch(
    theme=gr.themes.Soft(
        primary_hue="emerald",
        secondary_hue="slate",
        neutral_hue="neutral"
    ),
    css=css
)
