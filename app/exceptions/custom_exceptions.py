class UnauthorizedException(Exception):
    def __init__(self, message="Unauthorized"):
        self.message = message


class ForbiddenException(Exception):
    def __init__(self, message="Access denied"):
        self.message = message


class ResourceNotFoundException(Exception):
    def __init__(self, message="Resource not found"):
        self.message = message