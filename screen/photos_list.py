import gdata.gauth
import os
import pickle
import gdata.photos.service
from screen import config

def getPhotos():
    Scope='https://picasaweb.google.com/data/'

    def GetAuthToken():
        if os.path.exists(".token"):
            with open(".token") as f:
                token = pickle.load(f)
        else:
            token = gdata.gauth.OAuth2Token(client_id=config.clientid,client_secret=config.clientsecret,scope=Scope,user_agent=config.User_agent)
            print( token.generate_authorize_url(redirect_uri='urn:ietf:wg:oauth:2.0:oob'))
            code = raw_input('What is the verification code? ').strip()
            token.get_access_token(code)
            with open(".token", 'w') as f:
                pickle.dump(token, f)
        return token


    token = GetAuthToken()

    gd_client = gdata.photos.service.PhotosService()
    old_request = gd_client.request


    def request(operation, url, data=None, headers=None):
        headers = headers or {}
        headers['Authorization'] = 'Bearer ' + token.access_token
        return old_request(operation, url, data=data, headers=headers)
    #TODO if receive a 403, get a new token

    gd_client.request = request

    photos = gd_client.GetFeed('/data/feed/api/user/default/album/%s?kind=photo&imgmax=1024' % (config.album_name))

    # for photo in photos.entry:
    #     print "Photo: ", photo.title.text, ", url: ", photo.content.src
    #     print photo.content.src

    photosList = []
    for photo in photos.entry:
        photosList.append(photo.content.src)
    return photosList