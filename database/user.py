from postgrest.exceptions import APIError

from database.client import supabase
from utils.logger import logger


class User:
    """
    Класс для манипуляции данными юзера в базе данных.

    Args:
        user_id (any): Id юзера.
        server_id (any): Id сервера.
    """

    def __init__(self, user_id, server_id):
        self.user_id = user_id
        self.server_id = server_id

    def get_balance(self):
        """
        Возвращает баланс юзера.

        Returns:
            balance data (dict): Объект с балансом пользователя.
                * balance (int): Баланс пользователя

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки
        """

        try:
            response = (
                supabase.table("balances")
                .select("balance")
                .eq("user_id", self.user_id)
                .execute()
            )

            return {"balance": response.data[0]["balance"]}

        except IndexError:
            return {
                "error": "Пользователь не найден в базе данных.",
                "message": "База данных вернула пустой массив.",
            }

        except APIError as exc:
            return {
                "error": "Ошибка при обращении к базе данных.",
                "message": exc.message,
            }

        except Exception as exc:
            return {
                "error": "Внутренняя ошибка.",
                "message": exc,
            }

    def add_currency(self, amount: int):
        """
        Добавляет валюту к балансу пользователя с помощью RPC.

        Args:
            amount (int): Количество валюты которое необходимо добавить.

        Returns:
            new balance data (dict): Объект с обновленным балансом пользователя.
                * balance (int): Новый баланс пользователя.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки.
        """

        if amount <= 0:
            return {
                "error": "Некорректная сумма.",
                "message": "Сумма должна быть больше нуля.",
            }

        try:
            response = supabase.rpc(
                "add_currency",
                {
                    "p_user_id": self.user_id,
                    "p_server_id": self.server_id,
                    "p_amount": amount,
                },
            ).execute()

            if response.data is None:
                return {
                    "error": "Пользователь не найден в базе данных.",
                    "message": "База данных не вернула обновленный баланс.",
                }

            logger.info(
                f"К балансу пользователя добавлено {amount} | user_id: {self.user_id} | server_id: {self.server_id}"
            )

            return {"balance": response.data}

        except APIError as exc:
            return {
                "error": "Ошибка при обращении к базе данных",
                "message": exc.message,
            }

        except Exception as exc:
            return {
                "error": "Внутренняя ошибка.",
                "message": exc,
            }

    def remove_currency(self, amount: int):
        """
        Отнимает валюту от баланса пользователя. Функция **может** уменьшить баланс пользователя до отрицательных значений.

        Args:
            amount (int): Количество валюты которое нужно отнять.

        Returns:
            new balance data (dict): Объект с обновленным балансом пользователя.
                * balance (int): Новый баланс пользователя.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки.
        """

        if amount <= 0:
            return {
                "error": "Некорректная сумма.",
                "message": "Сумма должна быть больше нуля.",
            }

        try:
            response = supabase.rpc(
                "remove_currency",
                {
                    "p_user_id": self.user_id,
                    "p_server_id": self.server_id,
                    "p_amount": amount,
                },
            ).execute()

            if response.data is None:
                return {
                    "error": "Пользователь не найден в базе данных.",
                    "message": "База данных не вернула обновленный баланс.",
                }

            logger.info(
                f"От баланса пользователя отнято {amount} | user_id: {self.user_id} | server_id: {self.server_id}"
            )

            return {"balance": response.data}

        except APIError as exc:
            return {
                "error": "Ошибка при обращении к базе данных",
                "message": exc.message,
            }

        except Exception as exc:
            return {
                "error": "Внутренняя ошибка.",
                "message": exc,
            }

    def set_currency(self, amount):
        """
        Изменяет баланс пользователя. Функция **может** уменьшить баланс пользователя до отрицательных значений.

        Args:
            amount (int): Новое значение баланса.

        Returns:
            new balance data (dict): Объект с обновленным балансом пользователя.
                * balance (int): Новый баланс пользователя.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки.
        """
        try:
            response = (
                supabase.table("balances")
                .update({"balance": amount})
                .eq("user_id", self.user_id)
                .eq("server_id", self.server_id)
                .select("balance")
                .execute()
            )

            logger.info(
                f"Баланс пользователя изменен: {amount} | user_id: {self.user_id} | server_id: {self.server_id}"
            )

            return {"balance": response.data[0]["balance"]}

        except IndexError:
            return {
                "error": "Пользователь не найден в базе данных.",
                "message": "База данных вернула пустой массив.",
            }

        except APIError as exc:
            return {
                "error": "Ошибка при обращении к базе данных",
                "message": exc.message,
            }

        except Exception as exc:
            return {
                "error": "Внутренняя ошибка.",
                "message": exc,
            }
