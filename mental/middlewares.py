from channels.middleware import BaseMiddleware
import jwt
from urllib.parse import parse_qs

class JWTmiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract cookies from headers
        print(scope['headers'])
        try :
            cookies = scope['headers'][13]
        except :
            cookies = scope['headers'][10]
        print(cookies)
        decode_cookie = cookies[1].decode('utf-8')
        print(decode_cookie)
        try :
            cookie = dict(item.split('=') for item in decode_cookie.split('; '))
            access_token = cookie.get('access_token')
        except :
            access_token = None

        print(access_token)
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
