from datetime import datetime
from dataclasses import dataclass

@dataclass
class StatusEvent:

    document_id: str
    status_anterior: str
    status_novo: str
    timestamp: datetime