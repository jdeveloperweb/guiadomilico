from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Modelo de manager de User onde o email é a forma de acesso ao site não um username
    """
    def create_user(self, username, email, password, **extra_fields):
        """
        Cria a salva um User com um usuario, email e senha informados
        """
        if not username:
            raise ValueError(_('Um nome de usuário deve ser informado!'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, username, email, password, **extra_fields):
        ## Extra Field para dizer que o usuário ainda não verificou o email
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_trusty', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser deve ter is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser deve ter is_superuser = True.'))

        return self.create_user(username, email, password, **extra_fields)