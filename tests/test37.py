def get_user_greeting_v1(username):
    """Returns a greeting for a user."""
    if not isinstance(username, str):
        raise TypeError("Username must be a string.")
    return f"Hello, {username}!"

def generate_welcome_message_v1(person_name):
    """Generates a welcome message for a person."""
    if not isinstance(person_name, str):
        raise TypeError("Person's name must be a string.")
    return f"Hello, {person_name}!"