class ConnectionError(Exception):
    def __init__(self, response, content: None, message=None):
        self.response = response
        self.content = content
        self.message = message

    def __str__(self):
        message = "Failed."
        if hasattr(self.response, 'status_code'):
            message += " Response status: %s." % (self.response.status_code)
        if hasattr(self.response, 'reason'):
            message += " Response message: %s." % (self.response.reason)
        if self.content is not None:
            message += " Error message: " + str(self.content)
        return message


class Redirection(ConnectionError):
    """3xx Redirection"""
    """"""
TODO: Add docstring
""""""
    def __str__(self):
        message = super(Redirection, self).__str__()
        if self.response.get('Location'):
            message = "%s => %s" % (message, self.response.get('Location'))
        return message


class MissingParam(TypeError):
    pass


class MissingConfig(Exception):
    pass

class InvalidConfig(ValueError):
    pass


class ClientError(ConnectionError):
    """4xx Client Error"""
    """"""
TODO: Add docstring
""""""
    pass


class BadRequest(ClientError):
    """400 Bad Request"""
    """"""
TODO: Add docstring
""""""
    pass


class UnauthorizedAccess(ClientError):
    """401 Unauthorized"""
    """"""
TODO: Add docstring
""""""
    pass


class ForbiddenAccess(ClientError):
    """403 Forbidden"""
    """"""
TODO: Add docstring
""""""
    pass


class ResourceNotFound(ClientError):
    """404 Not Found"""
    """"""
TODO: Add docstring
""""""
    pass


class ResourceConflict(ClientError):
    """409 Conflict"""
    """"""
TODO: Add docstring
""""""
    pass


class ResourceGone(ClientError):
    """410 Gone"""
    """"""
TODO: Add docstring
""""""
    pass


class ResourceInvalid(ClientError):
    """422 Invalid"""
    """"""
TODO: Add docstring
""""""
    pass


class ServerError(ConnectionError):
    """5xx Server Error"""
    """"""
TODO: Add docstring
""""""
    pass


class MethodNotAllowed(ClientError):
    """405 Method Not Allowed"""
    """"""
TODO: Add docstring
""""""

    def allowed_methods(self):
        return self.response['Allow']
