from rest_framework.exceptions import APIException


class ProfileDoesNotExist(APIException):
    status_code = 404
    default_detail = 'The requested profile does not exist.'

class PlanDoesNotExist(APIException):
    status_code = 404
    default_detail = 'The requested plan does not exist.'
