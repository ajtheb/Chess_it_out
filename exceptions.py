class InvalidMove(Exception):
    def __init__(self, msg="Invalid move", *args: object) -> None:
        super().__init__(msg, *args)
    pass
