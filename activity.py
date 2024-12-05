# activity.py

def get_activity_types():
    """
    Returns a dictionary of activity types grouped into categories.
    """
    return {
        "Work/Professional": [
            "Writing/Editing",
            "Meetings",
            "Brainstorming",
            "Coding/Programming",
            "Administrative Tasks",
            "Email Management",
        ],
        "Personal Development": [
            "Reading",
            "Studying",
            "Writing Journals",
            "Learning New Skills",
        ],
        "Health and Fitness": [
            "Exercise/Workout",
            "Meditation",
            "Walking",
            "Yoga",
        ],
        "Household/Chores": [
            "Cleaning",
            "Cooking",
            "Grocery Shopping",
            "Childcare",
        ],
        "Leisure": [
            "Watching TV/Movies",
            "Gaming",
            "Socializing",
            "Hobbies (e.g., painting, music)",
        ],
        "Miscellaneous": [
            "Traveling/Commuting",
            "Resting/Relaxing",
            "Other",
        ],
    }
