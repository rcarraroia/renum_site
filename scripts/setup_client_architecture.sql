-- ============================================================
-- SCRIPT: Setup Client Architecture
-- Data: 22/12/2025
-- Objetivo: Implementar arquitetura definitiva de client_id
-- ============================================================

-- ============================================================
-- PASSO 1: Criar Cliente "RENUM (Interno)" com UUID fixo
-- ============================================================
INSERT INTO clients (
    id,
    company_name,
    cnpj,
    plan,
    status,
    created_at,
    updated_at
) VALUES (
    '00000000-0000-0000-0000-000000000000',
    'RENUM (Interno)',
    '00.000.000/0000-00',
    'enterprise',
    'active',
    NOW(),
    NOW()
) ON CONFLICT (id) DO UPDATE SET
    company_name = EXCLUDED.company_name,
    updated_at = NOW();

-- ============================================================
-- PASSO 2: Associar RENUS e ISA ao Cliente Interno
-- ============================================================

-- Atualizar agentes existentes que não têm client_id
UPDATE agents 
SET client_id = '00000000-0000-0000-0000-000000000000',
    updated_at = NOW()
WHERE client_id IS NULL;

-- Garantir que agentes com UUID fixo também tenham client_id
UPDATE agents 
SET client_id = '00000000-0000-0000-0000-000000000000',
    updated_at = NOW()
WHERE id IN (
    '00000000-0000-0000-0000-000000000001',  -- RENUS
    '00000000-0000-0000-0000-000000000002',  -- ISA
    '00000000-0000-0000-0000-000000000003'   -- Discovery
)
AND (client_id IS NULL OR client_id != '00000000-0000-0000-0000-000000000000');

-- ============================================================
-- PASSO 3: Verificar/Criar Cliente "Slim Quality"
-- ============================================================
INSERT INTO clients (
    company_name,
    cnpj,
    plan,
    status,
    created_at,
    updated_at
) VALUES (
    'Slim Quality',
    '12.345.678/0001-90',
    'pro',
    'active',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- ============================================================
-- PASSO 4: Validação - Listar todos os agentes e seus client_id
-- ============================================================
SELECT 
    a.id,
    a.name,
    a.slug,
    a.client_id,
    c.company_name as client_name,
    a.status
FROM agents a
LEFT JOIN clients c ON a.client_id = c.id
ORDER BY a.name;

-- ============================================================
-- PASSO 5: Verificar se há agentes sem client_id (DEVE RETORNAR 0)
-- ============================================================
SELECT COUNT(*) as agents_without_client
FROM agents 
WHERE client_id IS NULL;

-- ============================================================
-- PASSO 6: Listar todos os clientes
-- ============================================================
SELECT 
    id,
    company_name,
    cnpj,
    plan,
    status,
    created_at
FROM clients
ORDER BY company_name;
