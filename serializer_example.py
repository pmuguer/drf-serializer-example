from datetime import datetime
import io
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

    def __str__(self):
        return "Objeto Comment: self.email = {}".format(self.email)


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self):
        if self.is_valid():
            return Comment(**self.validated_data)
        else:
            raise ValidationError("Datos inválidos")

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance


comment = Comment(email='leila@gmail.com', content='foo bar')

# 1.1 Serialización, paso 1: objeto ---> serializer
object_comment_serializer = CommentSerializer(comment)
# 1.2 Serialización, paso 2: serializer ---> JSON (rendering)
comment_json = JSONRenderer().render(object_comment_serializer.data)

out_serializacion = """
================
1. Serialización
================

1.1. Serialización, paso 1: objeto ---> serializer
--------------------------------------------------

# object_comment_serializer = CommentSerializer(comment)

Notar que se puede acceder a .data:

El tipo de datos de <serializer>.data es: '{}'
El contenido es <serializer>.data es: '{}'

Nota: no se puede acceder a <serializer>.validated_data

1.2. Serialización, paso 2: serializer ---> JSON (render)
---------------------------------------------------------

# comment_json = JSONRenderer().render(object_comment_serializer.data)

El tipo de datos de JSONRenderer().render() es: '{}'
El resultadode JSONRenderer().render() es: '{}'
""".format(
    type(object_comment_serializer.data),
    object_comment_serializer.data,
    type(comment_json),
    comment_json
)

print(out_serializacion)

try:
    print("Intentando ejecutar .is_valid()")
    object_comment_serializer.is_valid()
except Exception as exc:
    print(exc)

# Ni validated data
try:
    print("\nIntentando acceder a .validated_data")
    object_comment_serializer.validated_data
except Exception as exc:
    print(exc)

# 2.1. Deserialización, paso 1: JSON ---> dict
stream = io.BytesIO(comment_json)
data = JSONParser().parse(stream)

# 2.2. Deserialización, paso 2: dict ---> serializer
data_comment_serializer = CommentSerializer(data=data)

# 2.3. Deserialización, paso 3: serializer ---> objeto
deserialized_object = data_comment_serializer.create()

out_deserializacion = """
==================
2. Deserialización
==================

2.1. Deserialización, paso 1: JSON ---> dict
--------------------------------------------

# stream = io.BytesIO(comment_json)
# data = JSONParser().parse(stream)

El tipo de datos de data es: '{}'
El contenido de data es: '{}'

2.2. Deserialización, paso 2: dict ---> serializer
--------------------------------------------------

# data_comment_serializer = CommentSerializer(data=data)

El tipo de datos de <serializer>.validated_data es: '{}'
El contenido de <serializer>.validated_data es: '{}'
El tipo de datos de <serializer>.data es: '{}'
El contenido de <serializer>.data es: '{}'

2.3. Deserialización, paso 3: serializer ---> objeto
----------------------------------------------------

# deserialized_object = data_comment_serializer.create()

""".format(
    type(data),
    data,
    type(data_comment_serializer.validated_data),
    data_comment_serializer.validated_data,
    type(data_comment_serializer.data),
    data_comment_serializer.data
)

print(out_deserializacion)
