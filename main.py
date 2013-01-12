import logging

import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.escape

from settings import facebook_app_key, facebook_app_secret, cookie_secret

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


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("Hello, " + self.current_user["name"])

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/auth/login", AuthLoginHandler),
    (r"/auth/logout", AuthLogoutHandler),
],
    cookie_secret = cookie_secret,
    login_url = "/auth/login",
)
 
if __name__ == "__main__":
    application.listen(18888)
    tornado.ioloop.IOLoop.instance().start()
