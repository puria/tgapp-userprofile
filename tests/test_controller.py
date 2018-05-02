from .base import configure_app, create_app


class MailTemplatesControllerTests(object):

    def setup(self):
        self.app = create_app(self.app_config, False)

    def test_index(self):
        resp = self.app.get('/')
        assert 'HELLO' in resp.text


# class TestMailTemplatesControllerSQLA(MailTemplatesControllerTests):
#     @classmethod
#     def setupClass(cls):
#         cls.app_config = configure_app('sqlalchemy')


class TestMailTemplatesControllerMing(MailTemplatesControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')
