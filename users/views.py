from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
import os
from django.conf import settings
import shutil
from django.db import transaction
from collections import Counter
from django.utils import timezone
from datetime import datetime,timedelta
from drf_spectacular.utils import extend_schema,extend_schema_serializer

User = get_user_model()

class UserAPI(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    logger = logging.getLogger('django')
    """ API View to create User """


    def post(self, request):
        """
        API View that to interact with User.

        Returns a user created object.
        """
        try:
            user = User.objects.get(pk=request.user.id)
            serialized = UserSerializer(data = request.data)
            if serialized.is_valid():
                user_obj = serialized.save(created_by=user, is_active=True)
                updated_serializer = serialized.data
                try:
                    if request.data.get('picture'):
                        new_name = 'media/images/profile_images/'+str(user_obj.id)+'.'+(serialized.data['picture'].split('.')[-1])
                        src = os.path.join(settings.BASE_DIR,serialized.data['picture'].lstrip('/'))
                        dest = os.path.join(settings.BASE_DIR,new_name)
                        os.rename(src, dest)
                        # os.rename(serialized.data['picture'].lstrip('/'), new_name)
                        updated_serializer['picture'] = new_name
                        user_obj.picture = new_name.replace('media/','')
                        user_obj.save()
                except Exception as e:
                    user_obj.delete()
                    return Response({'error': repr(e), 'error_code': 'H007', 'matched': 'N', 'data': {}}, status=400)

                return Response({'error': '', 'error_code': '', 'data': {"user": updated_serializer}}, status=200)
            else:
                error = ', '.join(['{0}:{1}'.format(k, str(v[0])) for k, v in serialized.errors.items()])
                return Response({'error': error, 'error_code': 'HS002', 'data': {}}, status=200)
        except Exception as error:
            return Response({'error': repr(error), 'error_code': 'H007', 'matched': 'N', 'data': {}}, status=400)

    def put(self, request,pk=None):
        """
        API View that to interact with User.

        Returns a user updated object. Pass is_active=false to deactivate a user.
        """
        try:
            if pk:
                if(User.objects.filter(id=pk).exists()):
                    user_obj = User.objects.get(id=pk)
                    data_dict = request.data.copy()
                    data_dict['parameter_id'] = pk
                    serializer = UserSerializer(user_obj, data=data_dict,partial=True)
                    if serializer.is_valid():
                        print("serializer.validated_data is ",serializer.validated_data)
                        serializer.save()
                        # data = User.objects.filter(pk=data.id).values('id','username')
                        return Response({'error': '', 'error_code': '', 'data': {"user": serializer.data}}, status=200)
                    else:
                        error = ', '.join(['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
                        return Response({'error': error, 'error_code': 'HS002', 'data': {}}, status=200)
                else:
                    return Response({'error': 'No user available for provided id', 'error_code': 'H008', 'matched': 'N', 'data': {}}, status=401)
        except Exception as error:
            return Response({'error': repr(error), 'error_code': 'H007', 'matched': 'N', 'data': {}}, status=400)

    def get(self, request):
        """
        API View that to interact with User.

        Returns all users.
        """
        try:
            users = User.objects.filter().values('id','username','first_name','last_name','father_name','email','user_type','is_active','date_joined','gender','company_name','unit','brigade').order_by('-id')
            return Response({'error': '', 'error_code': '', 'data': {"user":users}}, status=200)
        except Exception as error:
            return Response({'error': repr(error), 'error_code': 'H007', 'matched': 'N', 'data': {}}, status=400)


# class UpdateUserAPI(APIView):
#     """
#     API View that used to update User.

#     Returns a user updated object.
#     """
#     permission_classes = (IsAuthenticated, )
#     serializer_class = UserSerializer
#     logger = logging.getLogger('django')

    
# class GetUserAPI(APIView):

   
class CheckUserName(APIView):
    logger = logging.getLogger('django')

    def post(self, request):
        try:
            data=User.objects.filter(username=request.data["username"])
            if data.exists():
                return Response({'error': '', 'error_code': '', 'data': True, 'status':data[0].is_active}, status=200)

            else:
                return Response({'error': '', 'error_code': '', 'data': False}, status=200)

        except Exception as error:
            return Response({'error': repr(error), 'error_code': 'H007', 'matched': 'N', 'data': {}}, status=400)



class ServerTimeAPI(APIView):
    permission_classes = (IsAuthenticated, )
    logger = logging.getLogger('django')

    def get(self, request):
        try:
            current_time = datetime.now()
            current_server_time= current_time.strftime("%Y-%m-%dT%H:%M:%SZ") 

            return Response({'error': '', 'error_code': '','data': {"current_server_time":current_server_time}}, status=200)
        except Exception as error:
                return Response({'error': repr(error), 'error_code': 'H007', 'matched': 'N', 'data': {}}, status=400)
