class ClickHouseException(Exception):
    def __init__(self, msg: str):
        msg = "\n".join(msg.split(". "))
        super().__init__(msg)
