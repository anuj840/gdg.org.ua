import cherrypy


__all__ = ['AuthorizeTool']


class AuthorizeTool(cherrypy.Tool):

    def __init__(self):
        super().__init__('before_handler', self._fetch, priority=20)

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach(
            'on_end_resource', self._cleanup, priority=80
        )

    def _fetch(self):
        session = cherrypy.session
        request = cherrypy.request

        google_oauth_token = session.get('google_oauth_token')
        google_user = session.get('google_user')
        admin_user = session.get('admin_user')

        if not google_user:
            raise cherrypy.HTTPError(401, 'Please authorize')
        if not admin_user:
            raise cherrypy.HTTPError(403, 'Forbidden')

        request.admin_user = admin_user
        request.google_user = google_user
        request.google_oauth_token = google_oauth_token

    def _cleanup(self):
        try:
            del cherrypy.request.admin_user
            del cherrypy.request.google_user
            del cherrypy.request.google_oauth_token
        except AttributeError:
            # That means we got 401 or 403 and did not set that attributes
            pass
