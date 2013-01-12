import os
from eventlet.green import urllib2
import facebook

import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.escape

from image_processing import process_image
from download import get_photo_array
from settings import facebook_app_key, facebook_app_secret, cookie_secret
#from database import store_image 

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)

class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        my_url = (self.request.protocol + "://" + self.request.host +
                  "/auth/login?next=" +
                  tornado.escape.url_escape(self.get_argument("next", "/")))
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=my_url,
                client_id=facebook_app_key,
                client_secret=facebook_app_secret,
                code=self.get_argument("code"),
                callback=self._on_auth)
            return
        self.authorize_redirect(
            redirect_uri=my_url,
            client_id=facebook_app_key,
        )
    
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Facebook auth failed")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

class ProcessHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #self.write("Processing...")
        api = facebook.GraphAPI(self.current_user["access_token"])
        reference = urllib2.urlopen(self.get_argument("src")).read()
        components = get_photo_array(api, maxPhotos = 80)

        self.set_header("Content-Type", "image/jpg")
        result = process_image(reference, components)
        self.write(result)
        # store into data base
        #store_image(self.current_user["id"], result)

class ChooseHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        api = facebook.GraphAPI(self.current_user["access_token"])
        src_uri = api.get_connections(
            "me", 
            "picture", 
            redirect="false",
            type="large"
        )['data']['url']

        self.render("templates/choose.html",
                    user_name = self.current_user["name"],
                    profile_src = src_uri)

class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        api = facebook.GraphAPI(self.current_user["access_token"])
        reference = self.request.files["pic"][0]["body"]
        components = get_photo_array(api, maxPhotos = 10)

        self.set_header("Content-Type", "image/jpg")
        result = process_image(reference, components)
        self.write(result)
        
class MainHandler(BaseHandler):
    # For the index page
    def get(self):
        if self.current_user:
            self.redirect("/choose")
        else:
            self.render("templates/index.html")

    def post(self):
        return self.get()


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/choose", ChooseHandler),
    (r"/upload", UploadHandler),
    (r'/(favicon.ico)', tornado.web.StaticFileHandler, {'path': "/static/favicon.ico"}),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "/static/"}),
    (r"/process", ProcessHandler),
    (r"/auth/login", AuthLoginHandler),
    (r"/auth/logout", AuthLogoutHandler),
],
    cookie_secret = cookie_secret,
    login_url = "/auth/login",
    static_path = os.path.join(os.path.dirname(__file__), "static"),
)
 
if __name__ == "__main__":
    application.listen(18888)
    tornado.ioloop.IOLoop.instance().start()
