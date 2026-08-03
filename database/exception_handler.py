from postgrest.exceptions import APIError
from utils.logger import logger

API_ERRORS = {
    "works_server_id_name_key": {
        "error": "Название уже занято.",
        "message": "Работа с таким названием уже создана на этом сервере.",
    },
    "works_min_payout_check": {
        "error": "Некорректное минимальное вознаграждение.",
        "message": "Минимальное вознаграждение должно быть больше или равно нулю.",
    },
    "works_max_payout_check": {
        "error": "Некорректное максимальное вознаграждение.",
        "message": "Максимальное вознаграждение должно быть строго больше минимального.",
    },
}

# TODO добавить обработку дубликата ключей при регистрации серверов и юзеров 
def exception_handler(exc: Exception, func_log: str, args_log: dict = {}):
    """
    Обрабатывает ошибки подаваемые из конструкции try-except.

    Args:
        func_log (str): Название функции которое будет передано в логгер.
        args_log (dict): Полезные данные которые будут переданы в логгер (необязательно).
            * name (str): Название аргумента.
            * value (any): Значение аргумента.
    """

    log = ""

    for key, value in args_log.items():
        log += f" | {key}: {value}"

    if isinstance(exc, APIError):
        for key, value in API_ERRORS.items():
            if key in exc.message:
                return value

        logger.error(
            f"Необрабатываемая ошибка базы данных во время {func_log} | {exc.message}"
            + log
        )

        return {"error": "Ошибка при обращении к базе данных.", "message": exc.message}

    logger.error(
        f"Необрабатываемая внутренняя ошибка во время {func_log} | {exc}" + log
    )

    return {"error": "Внутренняя ошибка.", "message": exc}
