from typing import Optional


class BabelProxyError(Exception):
    """When babel proxy object points to a None object will raise this error"""

    def __init__(self, message: Optional[str] = None) -> None:
        self.message: str = "Proxy object points to an empty lookup instance"
        if message:
            self.message = message
        super().__init__("Proxy object points to an empty lookup instance")
