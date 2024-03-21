from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import StorageContext
import weaviate
from llama_index.readers.file import PDFReader
from pathlib import Path
import warnings
import argparse

warnings.filterwarnings("ignore", category=DeprecationWarning, module="weaviate")

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

auth_config = weaviate.AuthApiKey(api_key="kWBh8xlWQk9zJXsDBRWPLS7hxQJN0LeygKpb")
client = weaviate.Client(
    url="https://msalehi-j300lwqu.weaviate.network",
    auth_client_secret=auth_config
)


def read_pdf(path):
    documents = PDFReader().load_data(Path(path))
    print('*** document loaded successfully ***')
    print(f'number of pages: {len(documents)}')
    return documents


def chunk_text(loaded_texts, chunk_size=500, chunk_overlap=25):
    parser = SimpleNodeParser.from_defaults(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = parser.get_nodes_from_documents(loaded_texts)
    print(f'Data was chunked to a total of {len(chunks)} chunks. chunk size = {chunk_size}. overlap = {chunk_overlap}')
    return chunks


def indexer(chunks):
    vector_store = WeaviateVectorStore(
        weaviate_client=client, index_name="LlamaIndex"
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(
        chunks, storage_context=storage_context
    )

    print('Chunks successfully embedded and indexed in Weaviate VectorDB')
    return index


def main(file_path, chunk_size, chunk_overlap):
    loaded_texts = read_pdf(file_path)
    chunked_texts = chunk_text(loaded_texts, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    index = indexer(chunked_texts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process a PDF file to chunk and index its contents.")
    parser.add_argument("--pdf_file", type=str, required=True, help="Path to the PDF file")
    parser.add_argument("--chunk_size", type=int, default=500, help="Size of each text chunk")
    parser.add_argument("--overlap", type=int, default=25, help="Overlap between consecutive text chunks")

    args = parser.parse_args()

    main(args.pdf_file, args.chunk_size, args.overlap)
