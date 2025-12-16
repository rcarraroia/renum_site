-- Verificar usuários existentes
SELECT 
    id, 
    email, 
    role, 
    first_name,
    last_name,
    created_at 
FROM profiles 
ORDER BY created_at DESC 
LIMIT 10;

-- Verificar usuários na tabela auth.users
SELECT 
    id,
    email,
    created_at,
    confirmed_at,
    last_sign_in_at
FROM auth.users
ORDER BY created_at DESC
LIMIT 10;
