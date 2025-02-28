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

### Additional Upcoming Features

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

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Poetry

### Installation

Once you have Python installed, you can clone this repository to your local machine using the following command:

```bash
git clone
```

After cloning the repository, you can navigate to the `personal-log` directory and install the required dependencies using the following command:

```bash
poetry install
```

This will install all the required dependencies for the personal log system.

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

#### Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Daily Fleeting Thoughts",
  "description": "Capture fleeting thoughts throughout the day",
  "type": "object",
  "properties": {
    "thoughts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "content": {
            "type": "string",
            "description": "The fleeting thought content"
          },
          "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "When the thought was recorded"
          }
        },
        "required": ["content", "timestamp"]
      }
    }
  },
  "required": ["date", "thoughts"]
}
```

#### Sample

```json
{
  "thoughts": [
    {
      "content": "The sunset today reminded me of childhood memories at the beach. Need to call mom this weekend.",
      "timestamp": "2025-02-19T14:30:00Z"
    },
    {
      "content": "Must remember to pick up groceries on the way home. Running low on coffee.",
      "timestamp": "2025-02-19T16:45:00Z"
    }
  ]
}
```

### Intentions

This module is focused on setting intentions and goals for the day. It is a place to document what you want to achieve and how you plan to do it.

#### Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Daily Intentions and Priorities",
  "description": "Schema for daily intentions and priorities",
  "type": "object",
  "properties": {
    "intentions": {
      "type": "object",
      "properties": {
        "longTermGoals": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Long-term goals"
        },
        "shortTermGoals": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Short-term goals"
        },
        "affirmation": {
          "type": "string",
          "description": "Positive affirmation for the day, optional"
        }
      },
      "required": ["longTermGoals", "shortTermGoals"]
    },
    "priorities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "task": {
            "type": "string",
            "description": "Task description"
          },
          "alignment": {
            "type": "string",
            "description": "How task aligns with goals"
          }
        },
        "required": ["task", "alignment"]
      },
      "minItems": 1,
      "maxItems": 3
    }
  },
  "required": ["date", "intentions", "priorities"]
}
```

#### Sample

```json
{
  "intentions": {
    "longTermGoals": [
      "Build a sustainable online business",
      "Publish a book on personal development"
    ],
    "shortTermGoals": [
      "Publish four articles a week",
      "Increase website traffic by 20%"
    ],
    "affirmation": "I am grateful for the opportunities that come my way and I embrace them with an open heart."
  },
  "priorities": [
    {
      "task": "Complete the first draft of Article X",
      "alignment": "Aligns with short-term goal of publishing four articles a week"
    },
    {
      "task": "Optimize website SEO",
      "alignment": "Supports long-term goal of building a sustainable online business"
    },
    {
      "task": "Engage with audience on social media",
      "alignment": "Contributes to increasing website traffic"
    }
  ]
}
```

### Learning Journal

This module is designed to track your learning progress and document new insights or discoveries. It is a place to reflect on what you have learned and how it has impacted your life. The learning journal is based on cognitive science of learn, connect and reflect.

#### Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Learning Journal",
  "description": "Learnings throughout the day",
  "type": "object",
  "properties": {
    "learnings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "topic": {
            "type": "string",
            "description": "Brief topic or context"
          },
          "insight": {
            "type": "string",
            "description": "What was learned"
          },
          "connection": {
            "type": "string",
            "description": "How it connects to existing knowledge or how to apply it"
          }
        },
        "required": ["topic", "insight"]
      }
    }
  },
  "required": ["date", "learnings"]
}
```

#### Sample

```json
{
  "learnings": [
    {
      "topic": "React Performance",
      "insight": "useMemo can prevent expensive calculations from re-running on every render",
      "connection": "This will help optimize the data visualization component I'm working on"
    },
    {
      "topic": "Team Communication",
      "insight": "Starting messages with context helps remote team members understand requests better",
      "connection": "Will use this in Slack channels to reduce back-and-forth questions"
    },
    {
      "topic": "Productivity",
      "insight": "Taking breaks every 90 minutes aligns with natural energy cycles",
      "connection": "Can structure deep work sessions around this rhythm"
    }
  ]
}
```

### Reflections

This module is focused on reflecting on your day and capturing your thoughts and feelings. It is a place to process your experiences and gain insights into your emotions and behaviors.

#### Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Daily Reflection",
  "description": "Reflect on various aspects of the day",
  "type": "object",
  "properties": {
    "reflection": {
      "type": "object",
      "properties": {
        "thoughts_reflections": {
          "type": "string",
          "description": "Brief summary of fleeting thoughts and observations"
        },
        "learning_reflections": {
          "type": "object",
          "properties": {
            "keyTakeaways": {
              "type": "array",
              "description": "Main learnings and insights from the day",
              "items": {
                "type": "string",
                "description": "Key takeaway or insight 1"
              }
            },
            "actionItems": {
              "type": "array",
              "description": "Actionable items or next steps",
              "items": {
                "type": "string",
                "description": "Action item 1"
              }
            }
          },
          "required": ["keyTakeaways", "actionItems"]
        }
      }
    }
  },
  "required": ["date", "reflection"]
}
```

#### Sample

```json
{
  "reflections": {
    "thoughts_reflections": "Had a productive day with focused work blocks",
    "learning_reflections": {
      "keyTakeways": [
        "Learned about the useMemo hook in React",
        "Scheduled focus blocks in calendar",
        "Read about the benefits of journaling"
      ],
      "actionItems": [
        "Implement useMemo in the project",
        "Block time for journaling in the evening",
        "Create a weekly focus block schedule"
      ]
    }
  }
}
```

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

- What were the most significant events or experiences of the past month? What did you learn from them?
- What were your biggest accomplishments over the past month? How did they make you feel?
- What were your biggest challenges over the past month? How did you overcome them, and what did you learn in the process?
- What are you most grateful for in your life right now? Why?
- What goals or aspirations do you have for the upcoming month? How will you work towards them?
- What are some things that have been causing you stress or anxiety lately? How can you address these challenges and reduce their impact on your life?
- What have you been doing to take care of yourself, both physically and mentally? What changes could you make to improve your self-care routine?
- What are some new things you have learned or discovered over the past month? How have they expanded your knowledge or perspective?
- Who are the people in your life that you are most grateful for? How can you show your appreciation for them?
- What is one thing you can do in the upcoming month to step out of your comfort zone and try something new or challenging?
