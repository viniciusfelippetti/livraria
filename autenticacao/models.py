from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from comum.validators import valida_cpf


# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, cpf, email, nome, endereco, password=None):
        if not cpf:
            raise ValueError('Um CPF deve ser especificado')
        if not email:
            raise ValueError('Um e-mail deve ser especificado')
        if not nome:
            raise ValueError('Um nome deve ser especificado')
        if not endereco:
            raise ValueError('Um nome deve ser especificado')
        email_normalizado = self.normalize_email(email)
        usuario = self.model(cpf=cpf, email=email_normalizado, nome=nome, endereco=endereco)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, cpf, email, nome, endereco, password):
        usuario = self.create_user(cpf, email, nome, endereco, password)
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)

class Usuario(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome', 'email', 'endereco']

    cpf = models.CharField(
        max_length=11,
        unique=True,
        error_messages={'unique': 'Um usuário com esse cpf/cnpj já foi cadastrado.'},
        verbose_name='CPF/CNPJ',
        validators=[valida_cpf]
    )

    email = models.EmailField(
        unique=True,
        error_messages={'unique': 'Um usuário com esse e-mail já foi cadastrado.'},
        verbose_name='E-mail'
    )
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    def __str__(self):
        return f'{self.nome} ({self.cpf})'

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
