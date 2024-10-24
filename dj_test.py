import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        try:
            # Verify the token with Google's OAuth2 API
            id_info = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)

            # Extract user info from the token
            email = id_info['email']
            first_name = id_info.get('given_name', '')
            last_name = id_info.get('family_name', '')

            # Check if the user exists or create a new one
            user, created = User.objects.get_or_create(email=email, defaults={
                'first_name': first_name,
                'last_name': last_name
            })

            # Log the user in (if created or already exists)
            login(request, user)
            
            return Response({'status': 'success', 'message': 'User logged in', 'user_id': user.id})

        except ValueError:
            return Response({'status': 'error', 'message': 'Invalid token'}, status=400)