import re
import os
import openai
import openai.error
from dotenv import load_dotenv
from ...typing import sha256, Dict, get_type_hints

load_dotenv()
api_key_env = os.environ.get("OPENAI_API_KEY")
# openai.api_base = "https://chimeragpt.adventblocks.cc/api/v1"

url = 'https://api.openai.com'
model = [
    'gpt-3.5-turbo',
    'gpt-4'
]
supports_stream = True
needs_auth = False


def _create_completion(model: str, messages: list, stream: bool = True, api_key: str = None, **kwargs):
    openai.api_key = api_key if api_key else api_key_env
    if openai.api_key is None:
        yield "To use Chimera, you need to provide the API-KEY"
        return

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=stream
        )

        if (stream):
            for chunk in response:
                yield chunk.choices[0].delta.get("content", "")
        else:
            yield response.choices[0].message.get("content", "")

    except openai.error.APIError as e:
        detail_pattern = re.compile(r'{"detail":"(.*?)"}')
        match = detail_pattern.search(e.user_message)
        if match:
            error_message = match.group(1)
            print(error_message)
            yield error_message
        else:
            print(e.user_message)
            yield e.user_message


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
