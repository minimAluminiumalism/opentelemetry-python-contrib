import logging
import traceback
from .config import Config


def dont_throw(func):
    """
    捕获并记录异常的装饰器，防止插桩逻辑抛出
    """
    logger = logging.getLogger(func.__module__)

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.debug(
                "Ollama 插桩失败 %s，错误: %s",
                func.__name__,
                traceback.format_exc(),
            )
            if Config.exception_logger:
                Config.exception_logger(e)

    return wrapper 