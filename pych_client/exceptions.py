class ClickHouseException(Exception):
    def __init__(self, code: int, error: str, query: str):
        self.code = code
        self.error = error
        self.query = query
        msg = f"Query\n{self.query}\n\nError\n{self.error}"
        super().__init__(msg)
