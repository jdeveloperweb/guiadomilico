from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Modelo de manager de User onde o email é a forma de acesso ao site não um username
    """
    def _create_user(self, username, email, password, is_staff, is_supeuser, **extra_fields):
        """
        Cria a salva um User com um usuario, email e senha informados
        """
        if not username:
            raise ValueError(_('Um nome de usuário deve ser informado!'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff, is_superuser=is_superuser, is_active=True, **extra_fields)
        user.set_password(password)
        user.save()

        return user


    def create_user(self, username, email=None, password=None, **extra_fields):
        ## Extra Field para dizer que o usuário ainda não verificou o email
        extra_fields.setdefault('is_trusty', False)

        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        ## Extra Field para dizer que o usuário ainda não verificou o email
        extra_fields.setdefault('is_trusty', True)

        return self._create_user(username, email, password, True, True, **extra_fields)