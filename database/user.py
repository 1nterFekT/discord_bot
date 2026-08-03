import math
import random
from datetime import datetime, timezone

from database.client import supabase
from database.exception_handler import exception_handler
from database.server import Server
from utils.logger import logger

# TODO add, remove и set нужно прописать транзакции
class User:
    """
    Класс для манипуляции данными юзера в базе данных.

    Args:
        user_id (str | int): Id юзера.
        server_id (str | int): Id сервера.
    """

    def __init__(self, user_id: str | int, server_id: str | int):
        self.user_id = user_id
        self.server_id = server_id
        self.server_instance = Server(server_id=self.server_id)

    def get_balance(self) -> dict:
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
                .eq("server_id", self.server_id)
                .execute()
            )

            return {"balance": response.data[0]["balance"]}

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="user.get_balance",
                args_log={"user_id": self.user_id, "server_id": self.server_id},
            )

    def add_currency(self, amount: int) -> dict:
        """
        Добавляет валюту к балансу пользователя.

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

            logger.info(
                f"К балансу юзера добавлено {amount} | user_id: {self.user_id} | server_id: {self.server_id}"
            )

            return {"balance": response.data}

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="user.add_currency",
                args_log={"user_id": self.user_id, "server_id": self.server_id},
            )

    def remove_currency(self, amount: int) -> dict:
        """
        Отнимает валюту от баланса пользователя. Функция не даст балансу пользователя уйти в минус.

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
                logger.error(
                    f"Ошибка при удалении валюты пользователя: пользователь не найден в базе данных | user_id: {self.user_id} | server_id: {self.server_id}"
                )

                return {
                    "error": "Пользователь не найден в базе данных.",
                    "message": "База данных не вернула обновленный баланс.",
                }

            logger.info(
                f"От баланса пользователя отнято {amount} | user_id: {self.user_id} | server_id: {self.server_id}"
            )

            return {"balance": response.data}

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="user.remove_currency",
                args_log={"user_id": self.user_id, "server_id": self.server_id},
            )

    def set_currency(self, amount: int) -> dict:
        """
        Изменяет баланс пользователя.

        Args:
            amount (int): Новое значение баланса. Принимает в себя любое значение, даже если оно отрицательное.

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

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="user.set_currency",
                args_log={"user_id": self.user_id, "server_id": self.server_id},
            )

    def get_transactions(self) -> dict:
        """
        Возвращает все транзакции пользователя.

        Returns:
            transactions data (dict): Объект с транзакциями.
                * transactions (list): Список транзакций.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки.
        """

        try:
            response = (
                supabase.table("transactions")
                .select("*")
                .eq("server_id", self.server_id)
                .or_(f"sender_id.eq.{self.user_id},receiver_id.eq.{self.user_id}")
                .execute()
            )

            return {"transactions": response.data}

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="user.get_transactions",
                args_log={"user_id": self.user_id, "server_id": self.server_id},
            )

    def get_to_work(self, work_name: str) -> dict:
        """
        Отправляет юзера на работу. Если запись о последнем использовании работы отсутствует - создает новый.
        Если последнее использование работы < кулдауна работы - генерирует и выдает вознаграждение и обновляет кулдаун в базе.

        Args:
            work_name (str): Название работы

        Returns:
            cooldown data (dict): Обновленные данные о кулдауне и сумма награда.
                * cooldown (dict): Данные о кулдауне.
                * reward (int): Сумма награды.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки.
        """

        try:
            work = self.server_instance.get_work(work_name=work_name)

            if "error" in work:
                return work

            cooldown = (
                supabase.table("works_cooldowns")
                .select("*")
                .eq("work_id", work["id"])
                .eq("user_id", self.user_id)
                .execute()
            )

            reward = random.randint(work["min_payout"], work["max_payout"])

            if len(cooldown.data) == 0:
                self.add_currency(amount=reward)

                response = (
                    supabase.table("works_cooldowns")
                    .insert(
                        {
                            "work_id": work["id"],
                            "user_id": self.user_id,
                        }
                    )
                    .select("*")
                    .execute()
                )

                logger.info(
                    f"Пользователь отправлен на работу | work_id: {work['id']} | server_id: {self.server_id} | user_id: {self.user_id}"
                )

                return {"cooldown": response.data[0], "reward": reward}

            now = datetime.now(timezone.utc)
            last_work_at = datetime.fromisoformat(cooldown.data[0]["last_work_at"])
            elapsed = (now - last_work_at).total_seconds()

            if elapsed < work["cooldown"]:
                return {
                    "error": "Работа не доступна.",
                    "message": f"Вы сможете воспользоваться этой работой через {math.floor(work["cooldown"] - elapsed)}с.",
                }

            self.add_currency(amount=reward)

            response = (
                supabase.table("works_cooldowns")
                .update(
                    {
                        "last_work_at": now.isoformat(),
                    }
                )
                .eq("work_id", work["id"])
                .eq("user_id", self.user_id)
                .select("*")
                .execute()
            )

            logger.info(
                f"Пользователь отправлен на работу | work_id: {work['id']} | server_id: {self.server_id} | user_id: {self.user_id}"
            )

            return {"cooldown": response.data[0], "reward": reward}

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="user.get_to_work",
                args_log={
                    "user_id": self.user_id,
                    "server_id": self.server_id,
                    "work_name": work_name,
                },
            )
