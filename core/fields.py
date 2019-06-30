from rest_framework import serializers

class Base64Field(serializers.Field):
    def to_representation(self, value):
        # print(value)
        ret = value
        if isinstance(value, memoryview):
            ret = value.tobytes()
        return ret.decode('utf-8')

    def to_internal_value(self, data):
        # print(data)
        return data.encode('utf-8')
