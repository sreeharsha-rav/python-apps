# Personal Log

This is a modular personal log system that can be used to keep track of your daily activities, thoughts, and ideas. It is designed to be simple and easy to use, while still providing a lot of flexibility in terms of how you can organize your log entries.

## Table of Contents

- [Personal Log](#personal-log)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Modules](#modules)
    - [Fleeting Thoughts](#fleeting-thoughts)
    - [Intentions](#intentions)
    - [Learning Journal](#learning-journal)
    - [Reflection](#reflections)
  - [TODOs and Ideas for Future Development](#todos-and-ideas-for-future-development)
    - [Emotional Processing - Mental State Analysis](#emotional-processing---mental-state-analysis)
      - [Schema](#schema)
      - [Sample](#sample)
    - [Self-Awareness - Behavioral Patterns](#self-awareness---behavioral-patterns)
      - [Schema](#schema-1)
      - [Sample](#sample-1)
    - [Gratitude Journal - Positive Psychology](#gratitude-journal---positive-psychology)
    - [Weekly Review](#weekly-review)
    - [Monthly Reflection](#monthly-reflection)
      - [Sample](#sample-2)

## Features

- **Modular Design**: The log is divided into different modules, each of which focuses on a specific aspect of your life, such as intentions, gratitude, or reflection.
- **Flexible Structure**: Each module has its own schema, which defines the fields that can be included in a log entry. This allows you to customize the log to suit your needs.
- **JSON Format**: The log entries are stored in JSON format, which is easy to read and write, and can be easily processed by other programs.
- **Command-Line Interface**: The log can be accessed and edited using a simple command-line interface, which makes it easy to add new entries or search for existing ones.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Poetry

### Installation

<!-- Once you have Python installed, you can clone this repository to your local machine using the following command:

```bash
git clone
```

After cloning the repository, you can navigate to the `personal-log` directory and install the required dependencies using the following command:

```bash
poetry install
```

This will install all the required dependencies for the personal log system. -->

## Usage

<!-- To start the personal log system, you can run the following command:

```bash
poetry run python personal_log.py
```

This will start the command-line interface for the personal log system, where you can add new log entries, search for existing entries, or view the log in different formats. -->

## Modules

The personal log system is divided into different modules, each of which focuses on a specific aspect of your life. The following are some of the modules that are included in the system:

### Fleeting Thoughts

This module is designed to capture your fleeting thoughts and ideas throughout the day. It is a place to jot down quick notes, reminders, or insights that you want to remember.

### Intentions

### Learning Journal

### Reflections

## TODOs and Ideas for Future Development

### Emotional Processing - Mental State Analysis

Track and process emotions through body sensations and immediate thoughts, as this activates the brain's encoding process and helps in emotional regulation.

- Track energy levels and mental clarity
- Document stress triggers and responses
- Note physical sensations connected to emotions

#### Schema

```json
    "mentalState": {
      "type": "object",
      "properties": {
        "energy": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10,
          "description": "Current energy level"
        },
        "clarity": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10,
          "description": "Mental clarity"
        },
        "dominantEmotions": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "maxItems": 3,
          "description": "Primary emotions experienced"
        },
        "bodySignals": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Physical sensations noticed"
        }
      },
      "required": ["energy", "dominantEmotions"]
    },

```

#### Sample

```json
    "mentalState": {
    "energy": 7,
    "clarity": 8,
    "dominantEmotions": ["curious", "satisfied", "calm"],
    "bodySignals": ["relaxed shoulders", "steady breathing"]
  },
```

### Self-Awareness - Behavioral Patterns

Document surprises, frustrations, and failures across cognitive, emotional, and behavioral dimensions to strengthen neural pathways related to self-understanding.

- Record unexpected reactions
- Analyze decision-making processes
- Document successful strategies and areas for improvement

#### Schema

```json
    "behavioralPatterns": {
      "type": "object",
      "properties": {
        "triggers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "situation": {
                "type": "string"
              },
              "response": {
                "type": "string"
              },
              "insight": {
                "type": "string"
              }
            }
          }
        },
        "successfulStrategies": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "What worked well today"
        }
      }
    },
    "awareness": {
      "type": "object",
      "properties": {
        "surprises": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Unexpected events or realizations"
        },
        "patterns": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Recurring themes noticed"
        }
      }
    },
```

#### Sample

```json
    "behavioralPatterns": {
    "triggers": [
      {
        "situation": "Unexpected project deadline",
        "response": "Initial anxiety, then systematic planning",
        "insight": "Planning reduces stress response"
      }
    ],
    "successfulStrategies": [
      "Deep breathing before meetings",
      "Breaking tasks into smaller chunks"
    ]
  },
  "awareness": {
    "surprises": [
      "Handled criticism better than expected",
      "Found creative solution during walk"
    ],
    "patterns": [
      "More productive after morning exercise",
      "Better decisions when well-rested"
    ]
  },
```

### Gratitude Journal - Positive Psychology

### Weekly Review

### Monthly Reflection

#### Sample

What were the most significant events or experiences of the past month? What did you learn from them?
What were your biggest accomplishments over the past month? How did they make you feel?
What were your biggest challenges over the past month? How did you overcome them, and what did you learn in the process?
What are you most grateful for in your life right now? Why?
What goals or aspirations do you have for the upcoming month? How will you work towards them?
What are some things that have been causing you stress or anxiety lately? How can you address these challenges and reduce their impact on your life?
What have you been doing to take care of yourself, both physically and mentally? What changes could you make to improve your self-care routine?
What are some new things you have learned or discovered over the past month? How have they expanded your knowledge or perspective?
Who are the people in your life that you are most grateful for? How can you show your appreciation for them?
What is one thing you can do in the upcoming month to step out of your comfort zone and try something new or challenging?
