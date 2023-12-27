from datetime import datetime
import django
from django.db import models
from pytz import timezone

class Base(models.Model):
    esta_ttus=models.CharField    ('Estatus', max_length=1,  null=True, blank=True, default='')
    created  =models.DateTimeField(auto_now=False, null=True,auto_now_add=False,blank=True)
    updated  =models.DateTimeField(auto_now=False, null=True,auto_now_add=False,blank=True)
    deleted  =models.DateTimeField(auto_now=False, null=True,auto_now_add=False,blank=True)

    # def __str__(self):
    #     return self.name 
            
    class Meta:
        abstract = True

    # def delete(self):
    #     self.deleted = '2022-04-25'
    #     self.save()

    # def restore(self):
    #     self.deleted = timezone.now
    #     self.save()

    def perform_create(self, serializer):
        serializer.save(created = datetime.now())

    '''
        Gettting Today Date in format ('Y-m-d')
    '''
    def gettingTodaysDate(language=None):
        if language is not None:
            return datetime.today().strftime('%d-%m-%Y')
        return datetime.today().strftime('%Y-%m-%d')
    
    def roundNumber(_number):
        return round(_number,4)