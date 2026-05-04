import gradio as gr


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
        with gr.Blocks(theme=self.theme, css="""
            button[role="tab"] { color: #F8F0E2 !important; font-family: 'JetBrains Mono', monospace !important; background-color: transparent !important; }
            button[role="tab"]:hover { color: #FF5992 !important; }
            button[role="tab"][aria-selected="true"] { border-bottom: 2px solid #FF5992 !important; color: #FF5992 !important; }
            button.lg { background-color: #191919 !important; color: #FF5992 !important; font-family: 'JetBrains Mono', monospace !important; border: none !important; }
            button.lg.secondary { background-color: transparent !important; color: #F8F0E2 !important; border: 1px solid #555555 !important; font-family: 'JetBrains Mono', monospace !important; }
            label, .label-wrap span { color: #F8F0E2 !important; font-family: 'Mulish', sans-serif !important; }
        """) as demo:

            gr.HTML("""
<div style="background-color:#191919; padding:20px; display:flex; align-items:center; gap:16px; border-bottom:2px solid #FF5992;">
    <img src="/gradio_api/file=assets/logo.png" style="height:60px; width:auto;">
    <div>
        <h1 style="font-family:'JetBrains Mono',monospace; color:#F8F0E2; margin:0; font-size:28px; font-weight:700;">Ask Ash</h1>
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

        return demo

    def launch(self):
        demo = self.build_gradio_layout()
        demo.launch(allowed_paths=["assets"])
