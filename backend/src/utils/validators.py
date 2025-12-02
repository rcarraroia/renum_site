"""
Funções de validação para dados de negócio
"""
import re
from typing import Optional


def validate_phone(phone: str) -> bool:
    """
    Valida número de telefone brasileiro
    
    Aceita formatos:
    - (11) 98765-4321
    - 11987654321
    - +55 11 98765-4321
    
    Args:
        phone: Número de telefone
        
    Returns:
        True se válido, False caso contrário
    """
    # Remover caracteres não numéricos
    phone_clean = re.sub(r'\D', '', phone)
    
    # Validar: deve ter 10 ou 11 dígitos (com ou sem código país)
    if len(phone_clean) in [10, 11]:
        return True
    elif len(phone_clean) == 13 and phone_clean.startswith('55'):
        return True
    
    return False


def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF brasileiro
    
    Args:
        cpf: CPF a validar
        
    Returns:
        True se válido, False caso contrário
    """
    # Remover caracteres não numéricos
    cpf_clean = re.sub(r'\D', '', cpf)
    
    # CPF deve ter 11 dígitos
    if len(cpf_clean) != 11:
        return False
    
    # Validar se não é sequência repetida
    if cpf_clean == cpf_clean[0] * 11:
        return False
    
    return cpf_clean.isdigit()


def validate_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ brasileiro
    
    Args:
        cnpj: CNPJ a validar
        
    Returns:
        True se válido, False caso contrário
    """
    # Remover caracteres não numéricos
    cnpj_clean = re.sub(r'\D', '', cnpj)
    
    # CNPJ deve ter 14 dígitos
    if len(cnpj_clean) != 14:
        return False
    
    # Validar se não é sequência repetida
    if cnpj_clean == cnpj_clean[0] * 14:
        return False
    
    return cnpj_clean.isdigit()


def validate_document(document: str) -> bool:
    """
    Valida CPF ou CNPJ
    
    Args:
        document: CPF ou CNPJ a validar
        
    Returns:
        True se válido, False caso contrário
    """
    doc_clean = re.sub(r'\D', '', document)
    
    if len(doc_clean) == 11:
        return validate_cpf(document)
    elif len(doc_clean) == 14:
        return validate_cnpj(document)
    
    return False


def validate_email(email: str) -> bool:
    """
    Valida formato de email
    
    Args:
        email: Email a validar
        
    Returns:
        True se válido, False caso contrário
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def format_phone(phone: str) -> str:
    """
    Formata telefone para padrão brasileiro
    
    Args:
        phone: Telefone a formatar
        
    Returns:
        Telefone formatado: (11) 98765-4321
    """
    phone_clean = re.sub(r'\D', '', phone)
    
    if len(phone_clean) == 11:
        return f"({phone_clean[:2]}) {phone_clean[2:7]}-{phone_clean[7:]}"
    elif len(phone_clean) == 10:
        return f"({phone_clean[:2]}) {phone_clean[2:6]}-{phone_clean[6:]}"
    
    return phone


def format_cpf(cpf: str) -> str:
    """
    Formata CPF para padrão brasileiro
    
    Args:
        cpf: CPF a formatar
        
    Returns:
        CPF formatado: 123.456.789-00
    """
    cpf_clean = re.sub(r'\D', '', cpf)
    
    if len(cpf_clean) == 11:
        return f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"
    
    return cpf


def format_cnpj(cnpj: str) -> str:
    """
    Formata CNPJ para padrão brasileiro
    
    Args:
        cnpj: CNPJ a formatar
        
    Returns:
        CNPJ formatado: 12.345.678/0001-90
    """
    cnpj_clean = re.sub(r'\D', '', cnpj)
    
    if len(cnpj_clean) == 14:
        return f"{cnpj_clean[:2]}.{cnpj_clean[2:5]}.{cnpj_clean[5:8]}/{cnpj_clean[8:12]}-{cnpj_clean[12:]}"
    
    return cnpj
