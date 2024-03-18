from rest_framework import serializers
from users.models import User
from django.contrib.auth import get_user_model
import glob
import os
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import zipfile
from django.conf import settings
import base64
import csv
import io
from django.db.models import Q
from drf_spectacular.utils import extend_schema,extend_schema_serializer
from drf_extra_fields.fields import Base64ImageField

User = get_user_model()

@extend_schema_serializer(
    exclude_fields=('parameter_id','picture'), # schema ignore these fields
)
class UserSerializer(serializers.ModelSerializer):
    picture = Base64ImageField(required = False,allow_null=True)
    parameter_id = serializers.IntegerField(required = False)

    class Meta:
        model = User
        exclude = ('user_permissions','groups','last_login','is_superuser','is_staff','created_by')

    def to_representation(self, instance):
        """This is to ensure that the password is not being returned in api response"""
        ret = super().to_representation(instance)
        ret.pop('password')
        return ret

    def create(self, validated_data):
        return  User.objects.create_user(**validated_data)

    def update(self,instance,validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.father_name = validated_data.get('father_name', instance.father_name)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.brigade = validated_data.get('brigade', instance.brigade)
        instance.email = validated_data.get('email', instance.email)

        if(validated_data.get('picture')):
            # try/except added to pass the IsADirectoryError when initially organization didn't had the picture set
            try:
                if(glob.glob( 'media/images/profile_images/'+str(validated_data.get('parameter_id')) + '.*'  )):
                    os.remove(glob.glob( 'media/images/profile_images/'+str(validated_data.get('parameter_id')) + '.*'  )[0])
            except Exception as e:
                pass

        # instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
        return instance



