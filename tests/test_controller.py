from .base import configure_app, create_app


class UserProfileControllerTests(object):

    def setup(self):
        self.app = create_app(self.app_config, False)
        self.env = {'REMOTE_USER': 'manager'}

    def test_app_index(self):
        # needed to know that the application starts without errors with this pluggable
        r = self.app.get('/')
        assert 'HELLO' in r.text

    def test_index_anon(self):
        # if you're not logged in you should get a 401
        self.app.get('/userprofile', status=401)

    def test_index(self):
        r = self.app.get('/userprofile', extra_environ=self.env, status=200)
        assert 'Example Manager' in r.text, r.text


# SQLAlchemy is currently not supported, when the support is added decomment this and all tests
# should run even with sqlalchemy
# class TestUserProfileControllerSQLA(UserProfileControllerTests):
#     @classmethod
#     def setupClass(cls):
#         cls.app_config = configure_app('sqlalchemy')


class TestUserProfileControllerMing(UserProfileControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')
