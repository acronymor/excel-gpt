import openai
from openai.error import RateLimitError, InvalidRequestError, Timeout

from excelgpt.config.config import Config
from excelgpt.metric.time import calculate_time
from excelgpt.util.log import logger


class ChatGpt(object):
    def __init__(self) -> None:
        self._cfg: Config = Config()
        self.__temperature: int = self._cfg.openai_temperature
        self.__chat_model: str = self._cfg.openai_chat_model
        self.__openai_api_key: str = self._cfg.openai_key
        self.__openai_timeout: int = self._cfg.openai_timeout

    @calculate_time
    def say(self, messages: list[str]) -> str:
        openai.api_key = self.__openai_api_key
        try:
            response = openai.ChatCompletion.create(
                model=self.__chat_model,
                messages=messages,
                temperature=self.__temperature,
                request_timeout=self.__openai_timeout,
                stream=False
            )
        except InvalidRequestError as e1:
            logger.error("openai response={}".format(e1.json_body))
            return ""
        except (RateLimitError, Timeout) as e2:
            logger.error("openai key={}, response={}".format(self.__openai_api_key, e2.json_body))
            return ""

        return response.choices[0].message["content"]
