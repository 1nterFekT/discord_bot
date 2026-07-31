from database.client import supabase
from utils.logger import logger


def register_server(server_id):
    """
    Добавляет сервер в базу данных по его id.

    Args:
        server_id (any): Id сервера для добавления.

    Returns:
        server_data (dict): Объект с данными сервера из базы данных при успешной регистрации.
            * 'server' (dict): Объект с данными сервера из таблицы 'servers' базы данных.
            * 'settings' (dict): Объект с данными настроек сервера из таблицы 'servers_settings' базы данных.

        error_data (dict): Объект с информацией об ошибке, если таковая возникнет.
            * 'message' (str): Сообщение ошибки.
            * 'code' (str): Код ошибки.
            * 'hint' (str): Подсказка ошибки.
            * 'details' (str): Детали ошибки.
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

        logger.info(f"Новый сервер добавлен в базу данных, server_id: {server_id}")

        return {
            "server": servers_table_response.data[0],
            "settings": settings_table_response.data[0],
        }
    except Exception as exc:
        return exc


def register_user(user_id, server_id):
    """
    Добавляет юзера в базу данных по его id и id сервера, к которому будет привязан его баланс.

    Args:
        user_id (any): Id юзера для добавления.
        server_id (any): Id сервера для добавления.

    Returns:
        user_data (dict): Объект с данными юзера из базы данных при успешной регистрации.
            * 'user' (dict): Объект с данными юзера из таблицы 'users' базы данных.
            * 'balance' (dict): Объект с данными баланса юзера из таблицы 'balances' базы данных.

        error_data (dict): Объект с информацией об ошибке, если таковая возникнет.
            * 'message' (str): Сообщение ошибки.
            * 'code' (str): Код ошибки.
            * 'hint' (str): Подсказка ошибки.
            * 'details' (str): Детали ошибки.
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
            f"Новый юзер добавлен в базу данных, user_id: {user_id} (баланс прикреплен к server_id: {server_id})"
        )

        return {
            "user": users_table_response.data[0],
            "balance": balances_table_response.data[0],
        }
    except Exception as exc:
        return exc
