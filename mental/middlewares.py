from channels.middleware import BaseMiddleware
import jwt
from urllib.parse import parse_qs

class JWTmiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract cookies from headers
        query_string = scope['query_string'].decode('utf-8')  # e.g., "access_token=your-token-here"
        query_params = parse_qs(query_string)  # e.g., {'access_token': ['your-token-here']}
        access_token = query_params.get('access_token', [None])[0]  # Get the first value or None

        # Debug: Print to verify
        print("Query String:", query_string)
        print("Access Token:", access_token)

        # Process the token
        if access_token:
            try:
                token_data = self.decoder(access_token)
                scope['user'] = {
                    'id': token_data['user_id'],
                    'username': token_data['username']
                }
            except jwt.InvalidTokenError:
                scope['user'] = None
                print("Invalid token")
        else:
            scope['user'] = None
            print("No access token found")
        print("User:", scope['user'])
        return await super().__call__(scope, receive, send)
    def decoder(self , token) :
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
