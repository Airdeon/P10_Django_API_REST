from rest_framework.generics import CreateAPIView
from .serializers import UserSignupSerializer


# Create your views here.
class Signup(CreateAPIView):
    serializer_class = UserSignupSerializer
