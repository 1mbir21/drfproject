from tokenize import Token
import jwt
import requests
from django.http import JsonResponse
from django.conf import settings


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.method in ["GET", "POST", "PUT", "DELETE"]
            and "/admin/" not in request.path
        ):
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                pass

        response = self.get_response(request)
        return response
