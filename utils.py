
def ask_yes_no(question):
    """
    Asks the user a question that can be answered with yes or no.
    The function accepts various forms of input such as 'y', 'n', 'Ja', 'Yes', etc.

    Args:
        question (str): The question to be asked to the user.

    Returns:
        bool: True if the user answers affirmatively (yes), False if the user answers negatively (no).
    """
    # Define a set of valid affirmative and negative responses
    affirmative_responses = {'y', 'yes', 'ja', 'j', 'oui', 'si'}
    negative_responses = {'n', 'no', 'nein', 'n', 'non', ''}

    while True:
        # Ask the user the question and get the input
        user_input = input(question + " (yes/no): ").strip().lower()

        # Check if the user's input is in the affirmative or negative responses set
        if user_input in affirmative_responses:
            return True
        elif user_input in negative_responses:
            return False
        else:
            print("Invalid input. Please enter a valid yes or no response.")


def ask_additional_info():
    """
    Asks the user for additional information that can be used to help the model.

    Returns:
        str: The additional information provided by the user. + "This is important: " if the user provided any information.
    """
    additional_info = input(
        "Please enter any additional information you would like to provide to help the model (optional): ")
    # if additional_info is not empty, add "This is important: " to the beginning
    if additional_info.strip() != '':
        additional_info = f"This is important: {additional_info}"
    return additional_info
