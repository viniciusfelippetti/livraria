from django.core.exceptions import ValidationError
import re

def valida_cpf(valor):
    """ Validador de CPF """

    cpf = re.sub(r'\D', '', str(valor))

    if len(cpf) != 11 or cpf in [s * 11 for s in [str(n) for n in range(10)]]:
        raise ValidationError("CPF inválido.")

    # Calcula o primeiro dígito verificador
    soma_produtos = sum((i + 1) * int(cpf[i]) for i in range(9))
    primeiro_digito = soma_produtos % 11 % 10
    if int(cpf[9]) != primeiro_digito:
        raise ValidationError("CPF inválido.")

    # Calcula o segundo dígito verificador
    soma_produtos = sum(i * int(cpf[i]) for i in range(10))
    segundo_digito = soma_produtos % 11 % 10
    if int(cpf[10]) != segundo_digito:
        raise ValidationError("CPF inválido.")