import openai

OPEN_AI_ERRORS = (
    openai.APIError,
    openai.OpenAIError,
    openai.ConflictError,
    openai.NotFoundError,
    openai.APIStatusError,
    openai.RateLimitError,
    openai.APITimeoutError,
    openai.BadRequestError,
    openai.APIConnectionError,
    openai.AuthenticationError,
    openai.InternalServerError,
    openai.PermissionDeniedError,
    openai.LengthFinishReasonError,
    openai.UnprocessableEntityError,
    openai.APIResponseValidationError,
    openai.ContentFilterFinishReasonError,
)
