import gradio as gr

from core.config_loader import ConfigLoader
from core.drive_client import DriveClient
from core.file_registry import FileRegistry
from core.ingestion import DocumentParser, TextChunker, IngestionPipeline
from core.vector_store import VectorStore
from core.rag_chain import RAGChain
from layout import GradioLayout

def _init_components():
    config = ConfigLoader()
    drive_client = DriveClient(config.credentials_path)
    file_registry = FileRegistry()
    document_parser = DocumentParser()
    text_chunker = TextChunker(config)
    vector_store = VectorStore(config)
    ingestion_pipeline = IngestionPipeline(config, drive_client, file_registry, document_parser, text_chunker, vector_store)
    rag_chain = RAGChain(config, vector_store)
    return ingestion_pipeline, vector_store, rag_chain

def run_ingestion(ingestion_pipeline, vector_store):
    try:
        ingestion_pipeline.run()
    except Exception as e:
        if vector_store.vector_store._collection.count() == 0:
            raise Exception("Ingestion failed and vector store is empty. Please fix the issue and try again.")
        else:
            print(f"Warning: ingestion failed but existing index available. Error: {e}")

def main():
    ingestion_pipeline, vector_store, rag_chain = _init_components()
    run_ingestion(ingestion_pipeline, vector_store)
    with gr.Blocks() as demo:
        with gr.Tabs():
            with gr.Tab("Chat"):
                pass # chat components here
            with gr.Tab("Compare"):
                pass # compare components here
    demo.launch()

if __name__ == "__main__":
    main()
