from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny , IsAdminUser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_429_TOO_MANY_REQUESTS
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import FriendShipRequest
from .enums import RequestStatusEnum
from .serializers import FriendShipRequestSerializer
from UserAuthentication.serializers import UserSerializer
from UserAuthentication.models import User
from datetime import datetime , timedelta

class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            to_user_id = request.data.get('to_user')
            to_user = User.objects.get(id=to_user_id)
            from_user = request.user
            print(from_user)
            print(to_user)

            one_minute_ago = datetime.now() - timedelta(minutes=1)
            recent_requests = FriendShipRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count()
            if recent_requests >= 3:
                return Response({'error': 'You cannot send more than 3 friend requests in a minute'}, status=HTTP_429_TOO_MANY_REQUESTS)

            friend_request, created = FriendShipRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
            if not created:
                return Response({'error': 'Friend request already sent'}, status=HTTP_400_BAD_REQUEST)

            return Response({'message': 'Friend request sent successfully'}, status=HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=HTTP_404_NOT_FOUND)    
