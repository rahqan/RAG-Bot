# RAG-Bot


This project is a Streamlit application that allows users to upload multiple PDF documents, extract text from them, process the text into chunks, convert these chunks into embeddings, and store the embeddings in a vector database (Pinecone). Users can then interact with the app to query this data, and the app will return relevant chunks from the database.

## Features

1. **Upload PDFs**: Users can upload multiple PDF files.
2. **Extract Text**: The app extracts text from the uploaded PDFs.
3. **Text Chunking**: The extracted text is split into manageable chunks.
4. **Convert to Embeddings**: Text chunks are converted into vector embeddings using the INSTRUCTOR model.
5. **Store Embeddings**: Embeddings are stored in a Pinecone vector database.
6. **Query the Database**: Users can input queries, which are converted into vector embeddings and matched against the stored embeddings in the database.
7. **Display Results**: Relevant results from the database are displayed to the user.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Streamlit
- PyPDF2
- langchain-community
- InstructorEmbedding
- Pinecone
- dotenv

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pdf-chat-app.git
   cd pdf-chat-app
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up Pinecone and OpenAI API keys:
   - Create a `.env` file in the project root directory and add your Pinecone API key and OpenAI API key:

     ```
     PINECONE_API_KEY=your_pinecone_api_key
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501`.

3. Upload your PDF files using the file uploader.

4. Click on "Process" to extract text, convert to embeddings, and store them in Pinecone.

5. Input your query in the text box and click enter to get relevant results from the PDF documents.

## Functions

### `get_pdf_text(pdf_docs)`

- Extracts text from the uploaded PDF documents.
- **Parameters**: `pdf_docs` - List of uploaded PDF files.
- **Returns**: Extracted text from all PDF files as a single string.

### `get_text_chunks(raw_text)`

- Splits the extracted text into smaller chunks.
- **Parameters**: `raw_text` - Extracted text from the PDF files.
- **Returns**: List of text chunks.

### `convert_list_to_dict(input_list)`

- Converts a list into a dictionary.
- **Parameters**: `input_list` - List of text chunks.
- **Returns**: Dictionary where each key is an index, and the value is the corresponding text chunk.

### `get_web_text(url)`

- Extracts text from a webpage.
- **Parameters**: `url` - URL of the webpage.
- **Returns**: Extracted text from the webpage as a string.

### `to_vector_db(text_chunks)`

- Converts text chunks into embeddings and stores them in a Pinecone vector database.
- **Parameters**: `text_chunks` - List of text chunks.

### `query_to_vector(user_query)`

- Converts a user query into a vector embedding.
- **Parameters**: `user_query` - User's input query.
- **Returns**: Vector embedding of the user query.

### `relevant_search_in_db(vector_query)`

- Searches for relevant embeddings in the Pinecone vector database.
- **Parameters**: `vector_query` - Vector embedding of the user's query.
- **Returns**: Relevant results from the Pinecone database.

## Main Function

### `main()`

- The main function that runs the Streamlit app.
- Handles file uploads, processing of PDF text, conversion to embeddings, querying the database, and displaying results.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [PyPDF2](https://github.com/py-pdf/pypdf)
- [Pinecone](https://www.pinecone.io/)
- [InstructorEmbedding](https://github.com/UKPLab/instructor-embedding)

Feel free to contribute to the project or open issues if you find any bugs or have feature requests.

I added the url aspect so in future it can scrape websites and then maybe answer queries from web like Bing can.
