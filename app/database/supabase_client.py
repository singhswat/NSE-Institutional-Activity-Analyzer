from supabase import create_client, Client
from app.config.settings import settings

def get_supabase() -> Client:
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError(
            "Supabase settings missing. Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env"
        )

    return create_client(settings.supabase_url, settings.supabase_service_role_key)
