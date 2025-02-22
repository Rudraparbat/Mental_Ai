from channels.middleware import BaseMiddleware
import jwt

class JWTmiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract cookies from headers
        cookies = None
        for header_name, header_value in scope['headers']:
            if header_name == b'cookie':
                cookies = header_value.decode('utf-8')
                break

        # Parse cookies into a dictionary

        access_token = None
        if cookies:
            try :
                cookie_pairs = [pair.strip() for pair in cookies.split(';')]
                cookie_dict = dict(pair.split('=', 1) for pair in cookie_pairs if '=' in pair)
                access_token = cookie_dict.get('access_token')
            except Exception:
                access_token = None
        # Decode token and attach user info to scope
        if access_token:
            try:
                token_data = self.decoder(access_token)
                scope['user'] = {
                    'id': token_data['user_id'],
                    'username': token_data['username']
                }
            except jwt.InvalidTokenError:
                scope['user'] = None  # Invalid token, set user to None
        else:
            scope['user'] = None  # No token, set user to None
        # Call the next middleware or consumer
        return await super().__call__(scope, receive, send)

    def decoder(self, token):
        # Use your JWT secret key from settings for verification
        decoded_token = jwt.decode(
            token,
            options={"verify_signature": False},  # Replace with your secret key variable
            algorithms=["HS256"]      # Specify the algorithm used to sign the token
        )
        return decoded_token
