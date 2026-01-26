class Error(Exception):
    pass


class NoResticBinaryError(Error):
    pass


class ResticFailedError(Error):
    pass


class UnexpectedResticResponse(Error):
    pass
