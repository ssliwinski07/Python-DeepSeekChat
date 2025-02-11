import openai

OPEN_AI_ERRORS = (
    # API-related errors
    openai.APIError,  # Base class for API-specific errors
    openai.OpenAIError,  # Base class for all OpenAI-specific errors
    openai.APIConnectionError,  # Network or connection-related errors
    openai.APIResponseValidationError,  # Invalid API response
    openai.APIStatusError,  # Unexpected API status code
    openai.APITimeoutError,  # Request timeout
    # Authentication and permissions
    openai.AuthenticationError,  # Invalid API key or authentication
    openai.PermissionDeniedError,  # Insufficient permissions
    # Request-related errors
    openai.BadRequestError,  # Invalid request parameters
    openai.ConflictError,  # Resource conflict
    openai.NotFoundError,  # Resource not found
    openai.RateLimitError,  # Too many requests
    openai.UnprocessableEntityError,  # Request validation failed
    # Content-related errors
    openai.ContentFilterFinishReasonError,  # Content filtered by OpenAI
    openai.LengthFinishReasonError,  # Response exceeded max length
    openai.InternalServerError,  # OpenAI server error
)
