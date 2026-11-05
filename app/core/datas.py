from datetime import datetime, timezone
 
def agora_utc() -> datetime:

    """Devolve a data e hora atual no fuso horário UTC."""

    return datetime.now(timezone.utc)
 