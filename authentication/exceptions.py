from rest_framework.views import exception_handler

def core_exception_handler(exec, context):
    response = exception_handler(exec, context)
    handlers = {
        'ValidationError': _handle_generic_error,
        'NotAuthenticated': _handle_generic_error,
    }

    exception_class = exec.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exec, context, response)


def _handle_generic_error(exec, context, response):
    response.data = {
        'errors' : response.data
    }
    return response
