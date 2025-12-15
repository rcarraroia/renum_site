"""
Sprint 07A Validation Script
Validates that all components are properly implemented.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def check_file_exists(filepath: str) -> bool:
    """Check if file exists"""
    exists = Path(filepath).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {filepath}")
    return exists

def check_imports() -> bool:
    """Check if all modules can be imported"""
    print("\n🔍 Checking imports...")
    
    modules = [
        ("Integration Models", "src.models.integration"),
        ("Trigger Models", "src.models.trigger"),
        ("UazapiClient", "src.integrations.uazapi_client"),
        ("SMTPClient", "src.integrations.smtp_client"),
        ("SendGridClient", "src.integrations.sendgrid_client"),
        ("ClientSupabaseClient", "src.integrations.client_supabase"),
        ("IntegrationService", "src.services.integration_service"),
        ("TriggerService", "src.services.trigger_service"),
        ("TriggerEvaluator", "src.services.trigger_evaluator"),
        ("TriggerExecutor", "src.services.trigger_executor"),
        ("Celery App", "src.workers.celery_app"),
        ("Message Tasks", "src.workers.message_tasks"),
        ("Trigger Tasks", "src.workers.trigger_tasks"),
    ]
    
    all_ok = True
    for name, module_path in modules:
        try:
            __import__(module_path)
            print(f"✅ {name}")
        except Exception as e:
            print(f"❌ {name}: {e}")
            all_ok = False
    
    return all_ok

def main():
    print("=" * 60)
    print("SPRINT 07A - VALIDATION")
    print("=" * 60)
    
    print("\n📂 Checking files...")
    
    files = [
        # Migrations
        "backend/migrations/007_create_integrations_table.sql",
        "backend/migrations/008_create_triggers_table.sql",
        "backend/migrations/009_create_trigger_executions_table.sql",
        
        # Models
        "backend/src/models/integration.py",
        "backend/src/models/trigger.py",
        
        # Integration Clients
        "backend/src/integrations/__init__.py",
        "backend/src/integrations/uazapi_client.py",
        "backend/src/integrations/smtp_client.py",
        "backend/src/integrations/sendgrid_client.py",
        "backend/src/integrations/client_supabase.py",
        
        # Services
        "backend/src/services/integration_service.py",
        "backend/src/services/trigger_service.py",
        "backend/src/services/trigger_evaluator.py",
        "backend/src/services/trigger_executor.py",
        
        # Workers
        "backend/src/workers/__init__.py",
        "backend/src/workers/celery_app.py",
        "backend/src/workers/message_tasks.py",
        "backend/src/workers/trigger_tasks.py",
        
        # API Routes
        "backend/src/api/routes/integrations.py",
        "backend/src/api/routes/triggers.py",
        "backend/src/api/routes/webhooks.py",
        
        # Updated Tools
        "backend/src/tools/whatsapp_tool.py",
        "backend/src/tools/email_tool.py",
        "backend/src/tools/supabase_tool.py",
    ]
    
    files_ok = all(check_file_exists(f) for f in files)
    
    # Check imports
    imports_ok = check_imports()
    
    print("\n" + "=" * 60)
    if files_ok and imports_ok:
        print("✅ ALL CHECKS PASSED")
        print("\n📋 Next Steps:")
        print("1. Execute migrations in Supabase SQL Editor")
        print("2. Install Redis: sudo apt install redis-server")
        print("3. Test Celery worker: celery -A src.workers.celery_app worker --loglevel=info")
        print("4. Test Celery beat: celery -A src.workers.celery_app beat --loglevel=info")
        print("5. Start backend: python -m src.main")
        print("6. Test API endpoints with Postman/curl")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
