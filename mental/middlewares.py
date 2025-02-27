from channels.middleware import BaseMiddleware
import jwt
from urllib.parse import parse_qs

class JWTmiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract cookies from headers
        access_token = self.extract_access_token(scope['headers'])
        print("Access Token:", access_token)
        if access_token :
            token_data = self.decoder(access_token)
            scope['user'] ={
                'id' : token_data['user_id'],
                'username' : token_data['username']
            }
        print(scope['user'])
        return await super().__call__(scope , receive , send)
    def decoder(self , token) :
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    def extract_access_token(self, headers):
        # Convert headers list to dict
        headers_dict = dict(headers)
        
        # Get cookie header and decode it
        cookie_header = headers_dict.get(b'cookie', b'').decode('utf-8')
        if not cookie_header:
            print("No cookie header found")
            return None
        
        # Parse cookie string to find access_token
        for cookie in cookie_header.split('; '):
            if cookie.startswith('access_token='):
                return cookie.split('=', 1)[1]  # Split on first '=' only
        
        print("No access_token in cookies")
        return None