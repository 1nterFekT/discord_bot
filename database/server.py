from utils.logger import logger
from database.client import supabase
from database.exception_handler import exception_handler


class Server:
    """
    Класс для манипуляции данными сервера.

    Args:
        server_id (str | int): Id сервера.
    """

    def __init__(self, server_id: str | int):
        self.server_id = server_id

    def add_work(
        self,
        name: str,
        min_payout: int,
        max_payout: int,
        cooldown: int,
        description: str = None,
    ) -> dict:
        """
        Добавляет новую работу на сервер. Максимум работ на одном сервере - 25. На одном сервере не может существовать две работы с одинаковыми именами.

        Args:
            name (str): Название работы.
            min_payout (int): Минимальное вознаграждение.
            max_payout (int): Максимальное вознаграждение.
            cooldown (int): Кулдаун работы в секундах.

        Returns:
            created work data (dict): Данные о созданной работе.
                * work (dict): Данные о работе из базы данных.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки
        """

        server_works = self.get_all_works()["works"]

        if len(server_works) >= 25:
            return {
                "error": "Лимит количества работ.",
                "message": f"Количество работ на одном сервере не может превышать 25, на вашем сервере сейчас - {len(server_works)}.",
            }

        try:
            response = (
                supabase.table("works")
                .insert(
                    {
                        "server_id": self.server_id,
                        "name": name,
                        "description": description,
                        "min_payout": min_payout,
                        "max_payout": max_payout,
                        "cooldown": cooldown,
                    }
                )
                .select("*")
                .execute()
            )

            logger.info(
                f"Создана новая работа | server_id: {self.server_id} | id: {response.data[0]["id"]}"
            )

            return {"work": response.data[0]}

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="database.server.add_work",
                args_log={"server_id": self.server_id},
            )

    def remove_work(self, work_name: str) -> dict:
        """
        Удаляет работу по ее названию.

        Args:
            work_name (str): Название работы для удаления.

        Returns:
            success data (dict): Данные об удалении.
                * deleted_work (dict): Информация об удаленной работе.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки
        """

        try:
            response = (
                supabase.table("works")
                .delete()
                .eq("server_id", self.server_id)
                .eq("name", work_name)
                .select("*")
                .execute()
            )

            if len(response.data) == 0:
                return {
                    "error": "Работа не найдена.",
                    "message": "Работа с указанным именем не найдена.",
                }

            logger.info(
                f"Работа удалена | server_id: {self.server_id} | work_name: {work_name}"
            )

            return {"deleted_work": response.data[0]}

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="database.server.remove_work",
                args_log={"server_id": self.server_id},
            )

    def edit_work(
        self,
        work_name: str,
        name: str = None,
        description: str = None,
        min_payout: int = None,
        max_payout: int = None,
        cooldown: int = None,
    ) -> dict:
        """
        Обновляет работу по указанному названию.
        Все аргументы по дефолту **None** - если их не указывать, то эти поля работы в таблице базы данных не изменятся.

        Args:
            work_name (str): Название работы для изменения.
            name (str): Новое название работы.
            description (str): Новое описание работы.
            min_payout (int): Новое минимальное вознаграждение.
            max_payout (int): Новое максимальное вознаграждение.
            cooldown (int): Новый кулдаун.

        Returns:
            updated work data (dict): Обновленная информация о работе из базы данных.
                * work (dict): Обновленная работы из базы данных.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки
        """

        args = locals().items()
        fields_to_edit = {}

        for arg in args:
            key, value = arg

            if key not in ["self", "work_name"] and value is not None:
                fields_to_edit[key] = value

        try:
            response = (
                supabase.table("works")
                .update(fields_to_edit)
                .eq("server_id", self.server_id)
                .select("*")
                .execute()
            )

            if len(response.data) == 0:
                return {
                    "error": "Работа не найдена.",
                    "message": "Работы с указанным названием не существует.",
                }

            logger.info(
                f"Работа изменена | server_id: {self.server_id} | id: {response.data[0]["id"]}"
            )

            return {"work": response.data[0]}

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="database.server.get_all_works",
                args_log={"server_id": self.server_id},
            )

    def get_work(self, work_name: str) -> dict:
        """
        Отдает данные о работе по названию.

        Args:
            work_name (str): Название работы.

        Returns:
            work data (dict): Объект с информацией о работе.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки
        """

        try:
            response = (
                supabase.table("works")
                .select("*")
                .eq("server_id", self.server_id)
                .eq("name", work_name)
                .execute()
            )

            if len(response.data) == 0:
                return {
                    "error": "Работа не найдена.",
                    "message": "Работа с указанным названием не существует.",
                }

            return response.data[0]

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="database.server.get_work",
                args_log={"server_id": self.server_id, "work_name": work_name},
            )

    def get_all_works(self):
        """
        Отдает список всех работ сервера.

        Returns:
            works data (dict): Объект с данными о работах.
                * works (list): Список работ.

            error data (dict): Объект с информацией об ошибке.
                * error (str): Текст ошибки.
                * message (str): Детали ошибки
        """
        try:
            response = (
                supabase.table("works")
                .select("*")
                .eq("server_id", self.server_id)
                .execute()
            )

            return {"works": response.data}

        except Exception as exc:
            return exception_handler(
                exc=exc,
                func_log="database.server.get_all_works",
                args_log={"server_id": self.server_id},
            )
