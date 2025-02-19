# Fleeting Thoughts

A simple python application to take down fleeting thoughts and store them in a JSON file by the date.

The JSON schema is defined in [`schema.json`](./schema.json).

A sample entry based on the schema is defined in [`sample.json`](./sample.json).

## Usage

### Requirements

- Python 3.12 or higher
- Poetry

### Installation

```bash
poetry install
```

### Running the application

```bash
# Add a new thought
poetry run thoughts add "Need to remember to call Mom this weekend"

# List today's thoughts
poetry run thoughts list

# List thoughts for a specific date
poetry run thoughts list --date 2025-02-19

# List all thoughts
poetry run thoughts list-all
```

The thoughts are stored in a JSON file at `./entries/` folder by the date.
