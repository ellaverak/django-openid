from openid.models import User
from django.contrib.auth.hashers import make_password


class LoginBackend:
    """
        Class for custom authentication
    """
    def authenticate(self, request, userinfo=None, userdata=None):
        """
            Function for custom authentication
        """
        try:
            user = User.objects.get(email=userinfo['email'])
        except User.DoesNotExist:
            user = User(student_id=userdata['hyPersonStudentId'], username=userinfo['uid'], first_name=userinfo['given_name'],
                        last_name=userinfo['family_name'], email=userinfo['email'], password=make_password("test"))
            user.save()
            return user
        return user

    def get_user(self, user_id):
        """
            Helper function for custom authentication
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None