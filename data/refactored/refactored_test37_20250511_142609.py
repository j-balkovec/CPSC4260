def _common_logic_c5d5f9b22aa488117b4ca19bba5653dc(person_name):
    """Generates a welcome message for a person."""
    if not isinstance(person_name, str):
        raise TypeError("Person's name must be a string.")
    return f'Hello, {person_name}!'

def get_user_greeting_v1(username):
    return _common_logic_c5d5f9b22aa488117b4ca19bba5653dc(username)

def generate_welcome_message_v1(person_name):
    return _common_logic_c5d5f9b22aa488117b4ca19bba5653dc(person_name)