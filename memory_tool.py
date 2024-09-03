from tool import Tool
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any

@dataclass
class MemoryEntry:
    """
    A dataclass to store the value and the timestamp of the last update for a memory entry.
    
    Attributes:
    - value (Any): The value associated with the memory key.
    - timestamp (datetime): The time when the value was last updated.
    """
    value: Any
    update_timestamp: datetime = field(default_factory=datetime.now)
    use_timestamp: datetime = field(default_factory=datetime.now)

class MemoryManager(Tool):
    """
    A class to manage in-memory short key-value pairs along with their update timestamps.
    """

    def __init__(self) -> None:
        """
        Initializes the MemoryManager with an empty memory dictionary.
        """
        self.memory: dict[str, MemoryEntry] = {}

    def update_memory(self, key: str, value: str) -> None:
        """
        Updates the memory with a new short key-value pair. Make sure values are less than 200 characters.
        """
        if len(value) <200:
            self.memory[key] = MemoryEntry(value=value)

    def get_memory(self, key: str) -> str:
        """
        Retrieves the value associated with a given key from memory.
        """
        entry = self.memory.get(key, None)
        if entry:
            entry.use_timestamp = datetime.now()
            return entry.value
        return None

    def get_memory_snapshot(self) -> str:
        """
        Retrieves a formatted snapshot of the memory, showing keys, values and the time elapsed since their last update.
        """
        snapshot = []
        now = datetime.now()

        for key, entry in self.memory.items():
            elapsed_time = now - entry.update_timestamp
            formatted_time = self._format_timedelta(elapsed_time)
            snapshot.append(f"{key}: {entry.value} (updated {formatted_time} ago)")

        return "\n\n".join(snapshot)

    @staticmethod
    def _format_timedelta(td: timedelta) -> str:
        """
        Formats a timedelta object into a human-readable string.

        Args:
        - td (timedelta): The time difference to format.

        Returns:
        - str: A human-readable string representing the time difference.
        """
        days, seconds = td.days, td.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        formatted = f"{days}d {hours}h {minutes}m {seconds}s" if days > 0 else \
                    f"{hours}h {minutes}m {seconds}s" if hours > 0 else \
                    f"{minutes}m {seconds}s" if minutes > 0 else \
                    f"{seconds}s"
        
        return formatted