import os

def set_api_key_from_file():
    file_path="APIKEY.txt"
    """
    Read API key from a text file and set it as an environment variable.

    Args:
    - file_path (str): The path to the text file containing the API key.

    Returns:
    - bool: True if the API key was successfully read and set, False otherwise.
    """
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
            
        # Set the API key as an environment variable
        os.environ["OPENAI_API_KEY"] = api_key
        
        print(f"API key set successfully from {file_path}.")
        return True
    except Exception as e:
        print(f"Error setting API key from {file_path}: {e}")
        return False