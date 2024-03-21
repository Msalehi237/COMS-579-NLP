# Uploading a PDF File

To upload a PDF file, run the following command:

```bash
    python upload.py --pdf_file CongressionalBudgetJustification.pdf
```
Make sure the pdf file is in the same folder as upload.py.

You can also provide the following arguments to do more experiments:

```bash
    --chunk_size
    --overlap
```
Defaults are: chunk_size=500, overlap=25 


# Embedding Model

Embedding model used in this code is BGE-M3 (https://huggingface.co/BAAI/bge-m3). This model supports more language and longer texts which makes it a great choice for this work. 
  * Multi-Linguality: It can support more than 100 working languages.
  * Multi-Granularity: It is able to process inputs of different granularities, spanning from short sentences to long documents of up to 8192 tokens.


# Demo
If you need to access a demo video, you can find it [here](https://github.com/Msalehi237/COMS-579-NLP/blob/main/Demo.mp4). 
