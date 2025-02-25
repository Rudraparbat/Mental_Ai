from channels.middleware import BaseMiddleware
import jwt

class JWTmiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try :
            cookies = scope['headers'][13]
        except :
            cookies = scope['headers'][10]
        scopes = scope['headers']
        decode_cookie = cookies[1].decode('utf-8')
        try :
            cookies = dict(item.split('=') for item in decode_cookie.split('; '))
            access_token = cookies.get('access_token')
        except :
            access_token = None
        if access_token :
            token_data = self.decoder(access_token)
            scope['user'] ={
                'id' : token_data['id'],
                'username' : token_data['username']
            }
        return await super().__call__(scope , recieve , send)
    def decoder(self , token) :
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
