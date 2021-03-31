class Error(Exception):
    pass


class NoResticBinaryEror(Error):
    pass


class ResticFailedError(Error):
    pass


class UnexpectedResticResponse(Error):
    pass
