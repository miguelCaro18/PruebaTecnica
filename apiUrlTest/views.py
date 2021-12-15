from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import apiUrlTest.utilUrlText.readUrl as ReadU
import json

from apiUrlTest.utilUrlText.Exceptions import CustomException

from apiUrlTest.utilUrlText import validations




class FindURL(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self,request):
        response={}
        number_words=5

        # Pasar el request del usuario a formato json para validarlo, si no es correcto devuelve una petcción malformada
        try:
            json_data = json.loads(request.body)
        except:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "Malformed Request"
            }
            return JsonResponse(response)

        #Validar que los campos ingresador por el usuario sean de acuerdo a lo requerido en lo serializers
        validation = validations.validate_api(json_data)

        #Si no es valido se le envia el mensaje al usuario
        if not validation["success"]:
            response['message'] = validation["errors"]
            response['status'] = status.HTTP_400_BAD_REQUEST
            return JsonResponse(response)


        #Enviar la información recolectada a ultiUrl
        try:
            numReq=5
            if("number_words" in json_data.keys()):
                numReq=int(json_data['number_words'])
            answ= ReadU.getOnlyText(json_data['user_url'],numReq)
            response = {
                'status': status.HTTP_200_OK,
                'message': "Palabras",
                'content':answ
            }
            return JsonResponse(response)
        #En caso de un error envia la iformación
        except CustomException as e:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message':  e.args[0]
            }
            return JsonResponse(response)
