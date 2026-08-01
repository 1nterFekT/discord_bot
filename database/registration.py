from postgrest.exceptions import APIError

from database.client import supabase
from utils.logger import logger


def is_server_registered(server_id: str | int) -> dict:
    """
    Проверяет зарегистрирован ли сервер в базе данных.

    Args:
        server_id (str | int): Id сервера для проверки.

    Returns:
        server registration data (dict): Объект с данными о регистрации сервера.
            * 'registration_state' (bool): Статус регистрации сервера (True/False).

        error data (dict): Объект с информацией об ошибке.
            * error (str): Текст ошибки.
            * message (str): Детали ошибки
    """

    try:
        response = (
            supabase.table("servers").select("*").eq("server_id", server_id).execute()
        )

        if len(response.data) == 0:
            return {"registration_state": False}

        return {"registration_state": True}

    except APIError as exc:
        logger.error(
            f"Ошибка при проверке регистрации сервера: {exc.message} | server_id: {server_id}"
        )

        return {"error": "Ошибка при обращении к базе данных.", "message": exc.message}

    except Exception as exc:
        logger.error(
            f"Ошибка при проверке регистрации сервера: {exc} | server_id: {server_id}"
        )

        return {"error": "Внутренняя ошибка", "message": exc}


def is_user_registered(user_id: str | int) -> dict:
    """
    Проверяет зарегистрирован ли юзер в базе данных.

    Args:
        user_id (str | int): Id юзера для проверки.

    Returns:
        user registration data (dict): Объект с данными о регистрации юзера.
            * 'registration_state' (bool): Статус регистрации юзера (True/False).

        error data (dict): Объект с информацией об ошибке.
            * error (str): Текст ошибки.
            * message (str): Детали ошибки
    """

    try:
        response = supabase.table("users").select("*").eq("user_id", user_id).execute()

        if len(response.data) == 0:
            return {"registration_state": False}

        return {"registration_state": True}

    except APIError as exc:
        logger.error(
            f"Ошибка при проверке регистрации сервера: {exc.message} | user_id: {user_id}"
        )

        return {"error": "Ошибка при обращении к базе данных.", "message": exc.message}

    except Exception as exc:
        logger.error(
            f"Ошибка при проверке регистрации сервера: {exc} | user_id: {user_id}"
        )

        return {"error": "Внутренняя ошибка", "message": exc}


def register_server(server_id: str | int) -> dict:
    """
    Добавляет сервер в базу данных по его id.

    Args:
        server_id (str | int): Id сервера для добавления.

    Returns:
        server data (dict): Объект с данными сервера из базы данных при успешной регистрации.
            * 'server' (dict): Объект с данными сервера из таблицы 'servers' базы данных.
            * 'settings' (dict): Объект с данными настроек сервера из таблицы 'servers_settings' базы данных.

        error data (dict): Объект с информацией об ошибке.
            * error (str): Текст ошибки.
            * message (str): Детали ошибки
    """

    try:
        servers_table_response = (
            supabase.table("servers")
            .insert({"server_id": server_id})
            .select("*")
            .execute()
        )

        settings_table_response = (
            supabase.table("servers_settings")
            .insert({"server_id": server_id, "daily": 10000})
            .select("*")
            .execute()
        )

        logger.info(f"Новый сервер добавлен в базу данных: {server_id}")

        return {
            "server": servers_table_response.data[0],
            "settings": settings_table_response.data[0],
        }

    except APIError as exc:
        logger.error(
            f"Ошибка при регистрации нового сервера: {exc.message} | server_id: {server_id}"
        )

        return {"error": "Ошибка при обращении к базе данных.", "message": exc.message}

    except Exception as exc:
        logger.error(
            f"Ошибка при регистрации нового сервера: {exc} | server_id: {server_id}"
        )

        return {"error": "Внутренняя ошибка", "message": exc}


def register_user(user_id: str | int, server_id: str | int) -> dict:
    """
    Добавляет юзера в базу данных по его id и id сервера, к которому будет привязан баланс.

    Args:
        user_id (str | int): Id юзера для добавления.
        server_id (str | int): Id сервера для добавления.

    Returns:
        user data (dict): Объект с данными юзера из базы данных при успешной регистрации.
            * 'user' (dict): Объект с данными юзера из таблицы 'users' базы данных.
            * 'balance' (dict): Объект с данными баланса юзера из таблицы 'balances' базы данных.

        error data (dict): Объект с информацией об ошибке.
            * error (str): Текст ошибки.
            * message (str): Детали ошибки
    """

    try:
        users_table_response = (
            supabase.table("users").insert({"user_id": user_id}).select("*").execute()
        )

        balances_table_response = (
            supabase.table("balances")
            .insert({"user_id": user_id, "server_id": server_id, "balance": 0})
            .select("*")
            .execute()
        )

        logger.info(
            f"Новый юзер добавлен в базу данных: {user_id} | server_id: {server_id})"
        )

        return {
            "user": users_table_response.data[0],
            "balance": balances_table_response.data[0],
        }

    except APIError as exc:
        logger.error(
            f"Ошибка при регистрации нового юзера: {exc.message} | user_id: {user_id} | server_id: {server_id}"
        )

        return {"error": "Ошибка при обращении к базе данных.", "message": exc.message}

    except Exception as exc:
        logger.error(
            f"Ошибка при регистрации нового юзера: {exc} | user_id: {user_id} | server_id: {server_id}"
        )

        return {"error": "Внутренняя ошибка", "message": exc}
