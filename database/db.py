from supabase import create_client, Client

from config import SUPABASE_KEY, SUPABASE_URL
from utils.logger import logger

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def register_server(server_id):
    try:
        servers_response = (
            supabase.table("servers")
            .insert({"server_id": server_id})
            .select("*")
            .execute()
        )

        settings_response = (
            supabase.table("servers_settings")
            .insert({"server_id": server_id, "daily": 10000})
            .select("*")
            .execute()
        )

        logger.info(f"Новый сервер добавлен в базу данных: {server_id}")
        return {
            "server": servers_response.data[0],
            "settings": settings_response.data[0],
        }
    except Exception as exc:
        return exc


print(register_server(111))
