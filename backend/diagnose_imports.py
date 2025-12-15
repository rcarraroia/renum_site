"""
Script de diagnóstico para identificar qual import está travando
"""
import sys
import time

def test_import(module_name, timeout=3):
    """Testa import de um módulo com timeout"""
    print(f"Testing: {module_name}...", end=" ", flush=True)
    start = time.time()
    
    try:
        __import__(module_name)
        elapsed = time.time() - start
        print(f"✓ OK ({elapsed:.2f}s)")
        return True
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ FAIL ({elapsed:.2f}s): {e}")
        return False

# Lista de módulos para testar
modules = [
    "src.config.settings",
    "src.config.supabase",
    "src.utils.logger",
    "src.models.user",
    "src.services.auth_service",
    "src.api.middleware.auth_middleware",
    "src.api.routes.health",
    "src.api.routes.auth",
    "src.api.routes.clients",
    "src.api.routes.leads",
    "src.api.routes.projects",
    "src.api.routes.conversations",
    "src.api.routes.messages",
    "src.api.routes.interviews",
]

print("="*60)
print("IMPORT DIAGNOSTICS")
print("="*60)

for module in modules:
    test_import(module)
    
print("="*60)
print("Testing main app import...")
test_import("src.main")
