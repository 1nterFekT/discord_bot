from postgrest.exceptions import APIError

from database.client import supabase
from utils.logger import logger


def log_transaction(
    server_id: str | int,
    sender_id: str | int,
    receiver_id: str | int,
    amount: int,
    type: str = "Перевод",
    comment: str = None,
) -> dict:
    """
    Логирует транзакцию между пользователями или между пользователем и ботом в таблицу **transactions** базы данных.

    Args:
        server_id (str | int): Id сервера на котором произошла транзакция.
        sender_id (str | int): Id отправителя.
        receiver_id (str | int): Id получателя.
        amount (int): Сумма транзакции.
        type (str): Тип транзакции (перевод/выигрыш/проигрыш).
        comment (str): Комментарий транзакции (необязателен).

    Returns:
        transaction data (dict): Объект с информацией о транзакции.
            * transaction (dict): Информация о транзакции.

        error data (dict): Объект с информацией об ошибке.
            * error (str): Текст ошибки.
            * message (str): Детали ошибки
    """

    logger.info(f"Попытка логирования транзакции")

    try:
        response = (
            supabase.table("transactions")
            .insert(
                {
                    "server_id": server_id,
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    "amount": amount,
                    "type": type,
                    "comment": comment,
                }
            )
            .select("*")
            .execute()
        )

        logger.info(
            f"Успешное логирование транзакции | server_id: {server_id} | sender_id: {sender_id} | receiver_id: {receiver_id} | amount: {amount} | type: {type} | comment: {comment}"
        )

        return {"transaction": response.data[0]}

    except APIError as exc:
        logger.error(
            f"Ошибка при логировании транзакции: {exc.message} | server_id: {server_id} | sender_id: {sender_id} | receiver_id: {receiver_id} | amount: {amount} | type: {type} | comment: {comment}"
        )

        return {
            "error": "Ошибка при обращении к базе данных.",
            "message": exc.message,
        }

    except Exception as exc:
        logger.error(
            f"Ошибка при логировании транзакции: {exc} | server_id: {server_id} | sender_id: {sender_id} | receiver_id: {receiver_id} | amount: {amount} | type: {type} | comment: {comment}"
        )

        return {"error": "Внутренняя ошибка.", "message": exc}


def transfer(
    server_id: str | int,
    sender_id: str | int,
    receiver_id: str | int,
    amount: int,
    comment: str = None,
) -> dict:
    """
    Совершает перевод между пользователями с последующим логированием транзакции.

    Args:
        server_id (str | int): Id сервера на котором произошла транзакция.
        sender_id (str | int): Id отправителя.
        receiver_id (str | int): Id получателя.
        amount (int): Сумма транзакции.
        comment (str): Комментарий транзакции (необязателен).

    Returns:
        transaction data (dict): Объект с информацией о транзакции.
            * transaction (dict): Информация о транзакции.

        error data (dict): Объект с информацией об ошибке.
            * error (str): Текст ошибки.
            * message (str): Детали ошибки
    """

    logger.info(f"Попытка перевода валюты")

    try:
        supabase.rpc(
            "transfer",
            {
                "p_server_id": server_id,
                "p_sender_id": sender_id,
                "p_receiver_id": receiver_id,
                "p_amount": amount,
            },
        ).execute()

        transaction_log = log_transaction(
            server_id, sender_id, receiver_id, amount, "Перевод", comment
        )

        logger.info(
            f"Успешный перевод валюты | server_id: {server_id} | sender_id: {sender_id} | receiver_id: {receiver_id} | amount: {amount} | type: Перевод | comment: {comment}"
        )

        return {"transaction": transaction_log}

    except APIError as exc:
        logger.error(
            f"Ошибка при переводе валюты: {exc.message} | server_id: {server_id} | sender_id: {sender_id} | receiver_id: {receiver_id} | amount: {amount} | type: Перевод | comment: {comment}"
        )

        return {
            "error": "Ошибка при обращении к базе данных.",
            "message": exc.message,
        }

    except Exception as exc:
        logger.error(
            f"Ошибка при переводе валюты: {exc} | server_id: {server_id} | sender_id: {sender_id} | receiver_id: {receiver_id} | amount: {amount} | type: Перевод | comment: {comment}"
        )

        return {"error": "Внутренняя ошибка.", "message": exc}
