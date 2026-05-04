import gradio as gr
import time
import uuid


CUSTOM_CSS = """
    button[role="tab"] { color: #F8F0E2 !important; font-family: 'JetBrains Mono', monospace !important; background-color: transparent !important; font-size: 15px !important; padding: 10px 20px !important; }
    button[role="tab"]:hover { color: #FF5992 !important; }
    button[role="tab"][aria-selected="true"] { border-bottom: 2px solid #FF5992 !important; color: #FF5992 !important; }
    button.lg { background-color: #191919 !important; color: #FF5992 !important; font-family: 'JetBrains Mono', monospace !important; border: 1px solid #555555 !important; }
    button.lg.secondary { background-color: transparent !important; color: #F8F0E2 !important; border: 1px solid #555555 !important; font-family: 'JetBrains Mono', monospace !important; }
    label, .label-wrap span { color: #F8F0E2 !important; font-family: 'Mulish', sans-serif !important; }
    .tabs { margin-top: 16px !important; }
"""


class GradioLayout:
    def __init__(self, rag_chain, vector_store, config):
        self.rag_chain = rag_chain
        self.vector_store = vector_store
        self.config = config
        self.theme = gr.themes.Base(
            primary_hue=gr.themes.colors.neutral,
            font=gr.themes.GoogleFont("Mulish"),
            font_mono=gr.themes.GoogleFont("JetBrains Mono")
        )

    def build_gradio_layout(self):
        with gr.Blocks() as demo:

            gr.HTML("""
<div style="background-color:#191919; padding:20px 28px; display:flex; align-items:center; gap:16px; border-bottom:2px solid #FF5992; margin-bottom:8px;">
    <img src="/gradio_api/file=assets/logo.png" style="height:60px; width:auto;">
    <div>
        <h1 style="font-family:'JetBrains Mono',monospace; color:#F8F0E2; margin:0; font-size:28px; font-weight:700;">Ask Ash 🐾</h1>
        <p style="font-family:'Mulish',sans-serif; color:#FF5992; margin:0; font-size:14px;">Your local knowledge assistant</p>
    </div>
</div>
""")

            with gr.Tabs():

                with gr.Tab("Chat with Ash"):
                    self.model_dropdown = gr.Dropdown(
                        choices=self.config.available_models,
                        value=self.config.default_model,
                        label="Select Model"
                    )
                    self.question_input = gr.Textbox(
                        placeholder="Ask a question...",
                        label="Question",
                        lines=2
                    )
                    with gr.Row():
                        self.submit_btn = gr.Button("Submit", variant="primary")
                        self.clear_btn = gr.Button("Clear")
                    self.chatbot = gr.Chatbot(
                        label="Conversation",
                        height=400
                    )

                with gr.Tab("Compare Models"):
                    self.compare_question_input = gr.Textbox(
                        placeholder="Ask a question to compare models...",
                        label="Question",
                        lines=2
                    )
                    with gr.Row():
                        self.compare_submit_btn = gr.Button("Submit", variant="primary")
                        self.compare_clear_btn = gr.Button("Clear")
                    with gr.Row():
                        self.compare_model_1 = gr.Dropdown(
                            choices=self.config.available_models,
                            value=self.config.available_models[0],
                            label="Model 1"
                        )
                        self.compare_model_2 = gr.Dropdown(
                            choices=self.config.available_models,
                            value=self.config.available_models[1],
                            label="Model 2"
                        )
                    with gr.Row():
                        self.answer_box_1 = gr.Textbox(
                            label="Answer — Model 1",
                            interactive=False,
                            lines=10
                        )
                        self.answer_box_2 = gr.Textbox(
                            label="Answer — Model 2",
                            interactive=False,
                            lines=10
                        )
                    with gr.Row():
                        self.time_1 = gr.Textbox(
                            label="Response time",
                            interactive=False
                        )
                        self.time_2 = gr.Textbox(
                            label="Response time",
                            interactive=False
                        )

            self.submit_btn.click(
                fn=self.handle_chat,
                inputs=[self.question_input, self.model_dropdown, self.chatbot],
                outputs=[self.chatbot, self.question_input]
            )
            self.clear_btn.click(
                fn=lambda: ([], ""),
                inputs=[],
                outputs=[self.chatbot, self.question_input]
            )
            self.compare_submit_btn.click(
                fn=self.handle_compare,
                inputs=[self.compare_question_input, self.compare_model_1, self.compare_model_2],
                outputs=[self.answer_box_1, self.answer_box_2, self.time_1, self.time_2]
            )
            self.compare_clear_btn.click(
                fn=lambda: ("", "", "", "", ""),
                inputs=[],
                outputs=[self.compare_question_input, self.answer_box_1, self.answer_box_2, self.time_1, self.time_2]
            )

        return demo

    def handle_chat(self, question, model, history):
        if history is None:
            history = []

        docs = self.vector_store.similarity_search(question, self.config.top_k)
        context_parts = []
        sources = set()
        for doc in docs:
            filename = doc.metadata.get("file_name", "unknown")
            text = doc.page_content
            context_parts.append(f"[Source: {filename}]\n{text}")
            sources.add(filename)

        context = "\n\n".join(context_parts)

        chain = self.rag_chain.build_chain(model)
        result = chain.invoke(
            {"question": question, "context": context},
            config={"configurable": {"session_id": "chat_session"}}
        )

        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": result})
        return history, ""

    def handle_compare(self, question, model_1, model_2):
        docs = self.vector_store.similarity_search(question, self.config.top_k)
        context_parts = []
        sources = set()
        for doc in docs:
            filename = doc.metadata.get("file_name", "unknown")
            text = doc.page_content
            context_parts.append(f"[Source: {filename}]\n{text}")
            sources.add(filename)

        context = "\n\n".join(context_parts)

        session_1 = f"compare_1_{uuid.uuid4()}"
        session_2 = f"compare_2_{uuid.uuid4()}"

        chain_1 = self.rag_chain.build_chain(model_1)
        start_1 = time.time()
        result_1 = chain_1.invoke(
            {"question": question, "context": context},
            config={"configurable": {"session_id": session_1}}
        )
        time_1 = f"{time.time() - start_1:.2f}s"

        chain_2 = self.rag_chain.build_chain(model_2)
        start_2 = time.time()
        result_2 = chain_2.invoke(
            {"question": question, "context": context},
            config={"configurable": {"session_id": session_2}}
        )
        time_2 = f"{time.time() - start_2:.2f}s"

        return result_1, result_2, time_1, time_2

    def launch(self):
        demo = self.build_gradio_layout()
        demo.launch(
            allowed_paths=["assets"],
            theme=self.theme,
            css=CUSTOM_CSS
        )
