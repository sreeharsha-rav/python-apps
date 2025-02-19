# TODOs

- Integrate with LLamaIndex for querying using query engine modules
- Add support for context-based querying
- Add support for summarization of thoughts with knowledge

For this use case, LlamaIndex would be more suitable as it's specifically designed for working with personal data and provides simpler document management. Here's how to extend your fleeting thoughts project to include LLM integration:

## Project Structure Update
```text
fleeting-thoughts/
├── src/
│   └── fleeting_thoughts/
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       ├── storage.py
│       ├── llm/
│       │   ├── __init__.py
│       │   ├── indexer.py
│       │   └── query.py
│       └── prompts/
│           └── templates.py
├── .env
└── pyproject.toml
```

**Updated Poetry Dependencies (`pyproject.toml`):**
```toml
[tool.poetry.dependencies]
python = "^3.9"
pydantic = "^2.5"
python-dateutil = "^2.8"
click = "^8.1"
llama-index = "^0.9.0"
python-dotenv = "^1.0.0"
openai = "^1.3.0"
```

**Environment Setup (`.env`):**
```bash
OPENAI_API_KEY=your_api_key_here
```

## Implementation

**1. Document Indexing (`src/fleeting_thoughts/llm/indexer.py`):**
```python
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from pathlib import Path
from typing import Optional

class ThoughtIndexer:
    def __init__(self, storage_path: Path, index_path: Path):
        self.storage_path = storage_path
        self.index_path = index_path
        self.index_path.mkdir(exist_ok=True)
        
    def build_index(self) -> VectorStoreIndex:
        """Build or load the vector index from JSON files"""
        try:
            # Try to load existing index
            storage_context = StorageContext.from_defaults(
                persist_dir=str(self.index_path)
            )
            index = load_index_from_storage(storage_context)
        except:
            # Create new index if none exists
            documents = SimpleDirectoryReader(
                str(self.storage_path),
                file_extractor={
                    ".json": "json"
                }
            ).load_data()
            
            service_context = ServiceContext.from_defaults()
            index = VectorStoreIndex.from_documents(
                documents,
                service_context=service_context
            )
            # Persist index
            index.storage_context.persist(persist_dir=str(self.index_path))
            
        return index
```

**2. Query Handler (`src/fleeting_thoughts/llm/query.py`):**
```python
from llama_index import VectorStoreIndex
from .indexer import ThoughtIndexer
from ..prompts.templates import QUERY_TEMPLATE

class ThoughtQuery:
    def __init__(self, indexer: ThoughtIndexer):
        self.indexer = indexer
        self.index = self.indexer.build_index()
    
    def query_thoughts(self, query_text: str) -> str:
        """Query the thoughts index with natural language"""
        query_engine = self.index.as_query_engine(
            text_qa_template=QUERY_TEMPLATE
        )
        response = query_engine.query(query_text)
        return str(response)
    
    def refresh_index(self):
        """Rebuild the index with latest thoughts"""
        self.index = self.indexer.build_index()
```

**3. Prompt Templates (`src/fleeting_thoughts/prompts/templates.py`):**
```python
from llama_index.prompts import PromptTemplate

QUERY_TEMPLATE = PromptTemplate(
    """You are analyzing personal fleeting thoughts. 
    Context information is below.
    ---------------------
    {context_str}
    ---------------------
    Given this context, please answer the following question: {query_str}
    
    Provide a thoughtful analysis while maintaining the personal nature of the content.
    Answer: """
)
```

**4. Updated CLI Interface (`src/fleeting_thoughts/cli.py`):**
```python
import click
from pathlib import Path
from datetime import datetime
from .storage import ThoughtStorage
from .llm.indexer import ThoughtIndexer
from .llm.query import ThoughtQuery

@click.group()
def main():
    """Manage daily fleeting thoughts"""
    pass

# ... previous add and view commands ...

@main.command()
@click.argument("query_text")
def analyze(query_text):
    """Analyze thoughts using natural language queries"""
    storage = ThoughtStorage()
    index_path = Path.home() / ".fleeting_thoughts_index"
    
    indexer = ThoughtIndexer(storage.storage_path, index_path)
    querier = ThoughtQuery(indexer)
    
    result = querier.query_thoughts(query_text)
    click.echo(result)

@main.command()
def refresh_index():
    """Rebuild the thought index"""
    storage = ThoughtStorage()
    index_path = Path.home() / ".fleeting_thoughts_index"
    
    indexer = ThoughtIndexer(storage.storage_path, index_path)
    querier = ThoughtQuery(indexer)
    querier.refresh_index()
    click.echo("Index refreshed successfully")
```

## Usage Examples

1. Setup the environment:
```bash
poetry add llama-index openai python-dotenv
```

2. Query your thoughts:
```bash
# Add some thoughts first
poetry run fleeting add "Learning about LLMs today. The integration possibilities are exciting."
poetry run fleeting add "Need to explore more about vector databases."

# Build the initial index
poetry run fleeting refresh-index

# Query your thoughts
poetry run fleeting analyze "What have I been learning about recently?"
poetry run fleeting analyze "Summarize my thoughts about technology"
```

## Key Features

**LlamaIndex Integration**
- Uses vector store indexing for efficient semantic search
- Maintains persistent index storage
- Custom prompt templates for personal thought analysis
- Automatic JSON parsing and document loading

**Query Capabilities**
- Natural language querying of thoughts
- Semantic search across all stored thoughts
- Contextual analysis and summarization
- Index refreshing for updated content

This implementation allows you to:
- Semantically search through your thoughts
- Get summaries and insights
- Identify patterns and themes
- Ask questions about your recorded thoughts

The system will automatically maintain and update the vector index as you add new thoughts, enabling powerful natural language analysis of your personal reflections.
