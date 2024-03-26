from typing import List, Dict, Any
from litellm import completion, exceptions
import litellm

def llm_completion(messages: List[Dict[str, str]], model: str, **kwargs: Any) -> str:
    """
    Perform LLM text completion using LiteLLM.

    Args:
        messages (List[Dict[str, str]]): A list of message dictionaries, where each dictionary
            contains a "role" (str) and "content" (str) key-value pair.
        model (str): The name of the LiteLLM model to use for completion.
        **kwargs: Additional keyword arguments to pass to the LiteLLM completion function.
            Supported arguments include:
            - temperature (float): The sampling temperature for generating responses.
            - max_tokens (int): The maximum number of tokens to generate in the response.

    Returns:
        str: The generated completion response.

    Raises:
        litellm.LiteLLMError: If an error occurs during the completion process.
    """
    try:
        response = completion(model=model, messages=messages, **kwargs)
        return response
    except Exception as e:
        raise Exception(f"An error occurred during completion: {str(e)}") from e