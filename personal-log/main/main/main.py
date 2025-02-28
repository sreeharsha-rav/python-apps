# Example usage of the services
from datetime import datetime, date
from main.storage.json_file_manager import JSONFileManager
from main.modules.thoughts.model import Thought, Thoughts
from main.modules.thoughts.service import ThoughtsService
# from main.modules.learnings.model import Learning
# from main.modules.learnings.service import LearningsService
from main.modules.reflections.model import Reflection, LearningReflections
from main.modules.reflections.service import ReflectionsService

# Create file manager and services
file_manager = JSONFileManager("./data")
thoughts_service = ThoughtsService(file_manager)
# learnings_service = LearningsService(file_manager)
# intentions_service = IntentionsService(file_manager)
reflections_service = ReflectionsService(file_manager)

# # set a daily intention
# priority1 = Priority(task="Complete project milestone", alignment="Work towards long-term goal")
# priority2 = Priority(task="Exercise for 30 minutes", alignment="Improve health and well-being")
# priority3 = Priority(task="Read a chapter of a book", alignment="Personal growth")
# todays_intentions = Intentions(
#     long_term_goals=[
#         "Build a successful software company",
#         "Achieve work-life balance",
#         "Master system design"
#     ],
#     short_term_goals=[
#         "Complete current project by end of month",
#         "Learn a new programming language",
#         "Exercise 3 times a week"
#     ],
#     affirmation="I am capable of achieving my goals through consistent effort"
# )

# # You can create an instance like this:
# daily_intentions = DailyIntentions(
#     intentions=todays_intentions,
#     priorities=[priority1, priority2, priority3]
# )
# intentions_service.save_daily_intentions(daily_intentions)

# Add a thought
thought = Thought(
    content="this is a test thought 3",
    timestamp=datetime.now()
)
thoughts_service.add_thought(thought)

# # Add a learning
# learning = Learning(
#     topic="Python programming",
#     insight="Python is a versatile language used in web development, data science, and automation",
#     connection="I can use Python to build web applications and automate repetitive tasks",
# )
# learnings_service.add_learning(learning)

# Example usage for reflections with lists

# Create and save a complete reflection
learning_reflection = LearningReflections(
    key_takeaways=[
        "Learned about the importance of system design in scalable applications",
        "Discovered how to use Redis for caching to improve performance",
        "Understanding of microservices architecture improved"
    ],
    action_items=[
        "Research more about database sharding",
        "Practice implementing a load balancer",
        "Read chapter 3 of 'Designing Data-Intensive Applications'"
    ]
)

reflection = Reflection(
    thoughts_reflections="Today I realized the importance of taking short breaks to maintain focus",
    learning_reflections=learning_reflection
)

reflections_service.save_reflection(reflection)

# Example: Update learning reflection with lists
reflections_service.update_learning_reflection(
    key_takeaways=[
        "Today was about optimization - both in code and productivity",
        "Learned about React's useMemo hook for performance",
        "Discovered the importance of energy management throughout the day"  
    ],
    action_items=[
        "Implement useMemo in the dashboard component tomorrow",
        "Set up 90-minute focus blocks in calendar",
        "Try the Pomodoro technique with 25-minute work intervals"
    ]
)

# Example: Add individual items
reflections_service.add_key_takeaway("Communication is key in remote work environments")
reflections_service.add_action_item("Schedule weekly team sync meetings")

# Example 4: Retrieve and print a reflection
today_reflection = reflections_service.get_reflection()
if today_reflection:
    print("Today's reflection:")
    print(f"Thoughts: {today_reflection.thoughts_reflections}")
    
    if today_reflection.learning_reflections:
        print("\nKey takeaways:")
        for i, takeaway in enumerate(today_reflection.learning_reflections.key_takeaways, 1):
            print(f"  {i}. {takeaway}")
        
        print("\nAction items:")
        for i, action in enumerate(today_reflection.learning_reflections.action_items, 1):
            print(f"  {i}. {action}")
else:
    print("No reflection found for today")