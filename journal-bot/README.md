# Journal Bot

This a tool to help you journal your thoughts and feelings. It is a simple command line tool that will prompt you with questions and save your answers to a file.

It is modular and can be customized to fit your needs. You can add or remove modules to suit your preferences.

I based this tool on the [**Journal Framework**](journal_framework.md) I researched and developed. The framework is built on three fundamental psychological principles:

1. **Self-Determination Theory** - Supporting autonomy, competence, and relatedness
2. **Growth Mindset** - Viewing challenges as opportunities for learning
3. **Self-Compassion** - Treating oneself with the same kindness we'd offer a friend

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Poetry

### Installation

1. Clone the repository
2. Install dependencies with Poetry

```bash
poetry install
```

3. Run the tool

```bash
poetry run journal
```

### Customization

You can customize the tool by adding or removing modules. Each module is a Python file in the `modules` directory. You can add your own modules or remove existing ones.
You can also customize the questions by editing the `prompts.json` file in the `data` directory.

## Development Roadmap

**Version 0.1.0**

- [x] Create a basic command line tool
- [x] Add a module for gratitude journaling
- [x] Add a module for emotional check-ins
- [x] Add a module for future outlook
- [x] Add a module for growth mindset
- [ ] Modify poetry config for tool instead of package
- [ ] Enhance CLI interface
- [ ] Add aggregation and visualization of journal entries
- [ ] Add analysis of journal entries with NLP
- [ ] Add integration with LLMs for advanced reasoning

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
