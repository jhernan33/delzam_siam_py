from typing import Any


class PruebaMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print("Hola Middleware")
        return response
    
    def __process_view(self,request,view_func,view_args,view_kwargs):
        pass