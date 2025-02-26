from channels.middleware import BaseMiddleware
import jwt

class JWTmiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract cookies from headers
        cookies = None
        print(scope)
        for header_name, header_value in scope['headers']:
            if header_name == b'cookie':
                cookies = header_value.decode('utf-8')
                break

        # Parse cookies and extract access_token
        access_token = None
        if cookies:
            cookie_pairs = [pair.strip() for pair in cookies.split(';')]
            cookie_dict = dict(pair.split('=', 1) for pair in cookie_pairs if '=' in pair)
            access_token = cookie_dict.get('access_token')

        # Decode token and attach user info to scope
        if access_token:
            try:
                token_data = self.decoder(access_token)
                scope['user'] = {
                    'id': token_data['user_id'],  # Adjusted to match your token's field
                    'username': token_data['username']
                }
            except jwt.InvalidTokenError:
                scope['user'] = None
        else:
            scope['user'] = None
        print(scope['user'])
        return await super().__call__(scope, receive, send)
    def decoder(self , token) :
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
