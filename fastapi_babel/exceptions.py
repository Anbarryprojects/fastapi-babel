class BabelProxyError(Exception):
    """When babel proxy object points to a None object will raise this error"""
    def __init__(self, *args: object) -> None:
        super().__init__("Proxy object points to an empty lookup instance")