import re
import base64
import io, uuid
import os
from django.conf import settings
from PIL import Image

class ServiceImageView():

    @staticmethod
    def saveImag(arg,argDue):
        is_many = isinstance(arg,list)
        if is_many:
            listImages = arg
            ite=1
            obj_json = []
            place = os.path.realpath(settings.MEDIA_ROOT)
            for l in listImages:
                image = base64.b64decode(str(l['base']))
                img = Image.open(io.BytesIO(image))
                ext = '.'+img.format.lower()
                nameImage = str(uuid.uuid4())[:12]
                fileName = '0'+str(ite)+'-'+nameImage+'-'+str(ite)+ext
                imagePath = place +argDue+"/"+fileName
                img.save(imagePath)
                obj_json.append({'id':ite, 'image':fileName})
                ite +=1
            return obj_json
    
    @staticmethod
    def updateImage(arg,argDue,nameOfImageOld = None):
        is_many = isinstance(arg,list)
        if is_many:
            listImages = arg
            ite=0
            obj_json = []
            place = os.path.realpath(settings.MEDIA_ROOT)
            for l in listImages:
                ite +=1
                checkBase64 = re.search("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$", l['image'])
                if checkBase64:
                    # Save Base 64
                    image = base64.b64decode(str(l['image']))
                    img = Image.open(io.BytesIO(image))
                    ext = '.'+img.format.lower()
                    nameImage = str(uuid.uuid4())[:12]
                    fileName = '0'+str(ite)+'-'+nameImage+'-'+str(ite)+ext
                    imagePath = place +argDue+"/"+fileName
                    img.save(imagePath)
                    obj_json.append({'id':ite, 'image':fileName})
                    
                    # Remove Image Old
                    if nameOfImageOld is not None:
                        place = os.path.realpath(settings.MEDIA_ROOT)
                        cadena_image = nameOfImageOld
                        enviroment_string = argDue+'/'
                        length_enviroment = len(enviroment_string)
                        position_initial = cadena_image.find(enviroment_string)
                        image = cadena_image[position_initial +length_enviroment:len(cadena_image)]
                        recurso = place + enviroment_string + cadena_image
                        if os.path.exists(recurso):
                            os.remove(recurso)
                else:
                    cadena_image = l['image']
                    enviroment_string = argDue+'/'
                    length_enviroment = len(enviroment_string)
                    position_initial = cadena_image.find(enviroment_string)
                    image = cadena_image[position_initial +length_enviroment:len(cadena_image)]
                    recurso = place + enviroment_string + image
                    if l['delete']:    
                        if os.path.exists(recurso):
                            os.remove(recurso)
                        else:
                            print("Recurso no Existe")
                    else:
                        obj_json.append({'id':ite, 'image':image})
            return obj_json
        
    @staticmethod
    def removeImage(enviroment,image):
        place = os.path.realpath(settings.MEDIA_ROOT)
        cadena_image = image
        enviroment_string = enviroment+'/'
        length_enviroment = len(enviroment_string)
        position_initial = cadena_image.find(enviroment_string)
        image = cadena_image[position_initial +length_enviroment:len(cadena_image)]
        recurso = place + enviroment_string + image
        if os.path.exists(recurso):
            os.remove(recurso)
            return True
        else:
            return False