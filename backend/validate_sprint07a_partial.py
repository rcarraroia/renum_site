#!/usr/bin/env python3
"""
SPRINT 07A - Validação Parcial (Sem Uazapi)
Valida tudo que não depende da documentação completa da Uazapi
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all imports work"""
    print("\n" + "="*60)
    print("1. TESTING IMPORTS")
    print("="*60)
    
    errors = []
    
    # Models
    try:
        from src.models.integration import Integration, IntegrationCreate, IntegrationType
        print("✅ Models: Integration")
    except Exception as e:
        errors.append(f"❌ Models Integration: {e}")
        print(f"❌ Models: Integration - {e}")
    
    try:
        from src.models.trigger import (
            Trigger, TriggerCreate, TriggerCondition, TriggerAction,
            TriggerExecution, TriggerStatus
        )
        print("✅ Models: Trigger")
    except Exception as e:
        errors.append(f"❌ Models Trigger: {e}")
        print(f"❌ Models: Trigger - {e}")
    
    # Services
    try:
        from src.services.integration_service import IntegrationService
        print("✅ Services: IntegrationService")
    except Exception as e:
        errors.append(f"❌ Services IntegrationService: {e}")
        print(f"❌ Services: IntegrationService - {e}")
    
    try:
        from src.services.trigger_service import TriggerService
        print("✅ Services: TriggerService")
    except Exception as e:
        errors.append(f"❌ Services TriggerService: {e}")
        print(f"❌ Services: TriggerService - {e}")
    
    try:
        from src.services.trigger_evaluator import TriggerEvaluator
        print("✅ Services: TriggerEvaluator")
    except Exception as e:
        errors.append(f"❌ Services TriggerEvaluator: {e}")
        print(f"❌ Services: TriggerEvaluator - {e}")
    
    try:
        from src.services.trigger_executor import TriggerExecutor
        print("✅ Services: TriggerExecutor")
    except Exception as e:
        errors.append(f"❌ Services TriggerExecutor: {e}")
        print(f"❌ Services: TriggerExecutor - {e}")
    
    # Integration Clients (exceto Uazapi)
    try:
        from src.integrations.smtp_client import SMTPClient
        print("✅ Integration Clients: SMTPClient")
    except Exception as e:
        errors.append(f"❌ Integration SMTPClient: {e}")
        print(f"❌ Integration Clients: SMTPClient - {e}")
    
    try:
        from src.integrations.sendgrid_client import SendGridClient
        print("✅ Integration Clients: SendGridClient")
    except Exception as e:
        errors.append(f"❌ Integration SendGridClient: {e}")
        print(f"❌ Integration Clients: SendGridClient - {e}")
    
    try:
        from src.integrations.client_supabase import ClientSupabaseClient
        print("✅ Integration Clients: ClientSupabaseClient")
    except Exception as e:
        errors.append(f"❌ Integration ClientSupabaseClient: {e}")
        print(f"❌ Integration Clients: ClientSupabaseClient - {e}")
    
    # Workers
    try:
        from src.workers.celery_app import celery_app
        print("✅ Workers: celery_app")
    except Exception as e:
        errors.append(f"❌ Workers celery_app: {e}")
        print(f"❌ Workers: celery_app - {e}")
    
    try:
        from src.workers.message_tasks import send_whatsapp_message, send_email
        print("✅ Workers: message_tasks")
    except Exception as e:
        errors.append(f"❌ Workers message_tasks: {e}")
        print(f"❌ Workers: message_tasks - {e}")
    
    try:
        from src.workers.trigger_tasks import trigger_scheduler
        print("✅ Workers: trigger_tasks")
    except Exception as e:
        errors.append(f"❌ Workers trigger_tasks: {e}")
        print(f"❌ Workers: trigger_tasks - {e}")
    
    # API Routes
    try:
        from src.api.routes.integrations import router as integrations_router
        print("✅ API Routes: integrations")
    except Exception as e:
        errors.append(f"❌ API Routes integrations: {e}")
        print(f"❌ API Routes: integrations - {e}")
    
    try:
        from src.api.routes.triggers import router as triggers_router
        print("✅ API Routes: triggers")
    except Exception as e:
        errors.append(f"❌ API Routes triggers: {e}")
        print(f"❌ API Routes: triggers - {e}")
    
    try:
        from src.api.routes.webhooks import router as webhooks_router
        print("✅ API Routes: webhooks")
    except Exception as e:
        errors.append(f"❌ API Routes webhooks: {e}")
        print(f"❌ API Routes: webhooks - {e}")
    
    # Tools
    try:
        from src.tools.whatsapp_tool import WhatsAppTool
        print("✅ Tools: WhatsAppTool")
    except Exception as e:
        errors.append(f"❌ Tools WhatsAppTool: {e}")
        print(f"❌ Tools: WhatsAppTool - {e}")
    
    try:
        from src.tools.email_tool import EmailTool
        print("✅ Tools: EmailTool")
    except Exception as e:
        errors.append(f"❌ Tools EmailTool: {e}")
        print(f"❌ Tools: EmailTool - {e}")
    
    try:
        from src.tools.supabase_tool import SupabaseTool
        print("✅ Tools: SupabaseTool")
    except Exception as e:
        errors.append(f"❌ Tools SupabaseTool: {e}")
        print(f"❌ Tools: SupabaseTool - {e}")
    
    return errors


def test_encryption():
    """Test encryption/decryption"""
    print("\n" + "="*60)
    print("2. TESTING ENCRYPTION")
    print("="*60)
    
    errors = []
    
    try:
        from src.services.integration_service import IntegrationService
        
        service = IntegrationService()
        
        # Test data
        test_data = {
            "api_key": "test_key_123",
            "api_secret": "test_secret_456",
            "password": "test_password_789"
        }
        
        # Encrypt
        encrypted = service.encrypt_credentials(test_data)
        print(f"✅ Encryption works (type: {type(encrypted)})")
        
        # Decrypt
        decrypted = service.decrypt_credentials(encrypted)
        print(f"✅ Decryption works")
        
        # Verify
        if decrypted == test_data:
            print("✅ Encryption/Decryption verified (data matches)")
        else:
            errors.append("❌ Encryption/Decryption: data mismatch")
            print("❌ Data mismatch after encryption/decryption")
            
    except Exception as e:
        errors.append(f"❌ Encryption test: {e}")
        print(f"❌ Encryption test failed: {e}")
    
    return errors


def test_trigger_evaluator():
    """Test trigger condition evaluation"""
    print("\n" + "="*60)
    print("3. TESTING TRIGGER EVALUATOR")
    print("="*60)
    
    errors = []
    
    try:
        from src.services.trigger_evaluator import TriggerEvaluator
        from src.models.trigger import TriggerCondition
        
        evaluator = TriggerEvaluator()
        
        # Test 1: Simple equality
        condition = TriggerCondition(
            field="status",
            operator="equals",
            value="active"
        )
        context = {"status": "active"}
        
        if evaluator.evaluate_condition(condition, context):
            print("✅ Evaluator: equals operator works")
        else:
            errors.append("❌ Evaluator: equals operator failed")
            print("❌ Evaluator: equals operator failed")
        
        # Test 2: Greater than
        condition = TriggerCondition(
            field="count",
            operator="greater_than",
            value=10
        )
        context = {"count": 15}
        
        if evaluator.evaluate_condition(condition, context):
            print("✅ Evaluator: greater_than operator works")
        else:
            errors.append("❌ Evaluator: greater_than operator failed")
            print("❌ Evaluator: greater_than operator failed")
        
        # Test 3: Contains
        condition = TriggerCondition(
            field="message",
            operator="contains",
            value="hello"
        )
        context = {"message": "hello world"}
        
        if evaluator.evaluate_condition(condition, context):
            print("✅ Evaluator: contains operator works")
        else:
            errors.append("❌ Evaluator: contains operator failed")
            print("❌ Evaluator: contains operator failed")
            
    except Exception as e:
        errors.append(f"❌ Trigger evaluator test: {e}")
        print(f"❌ Trigger evaluator test failed: {e}")
    
    return errors


def test_smtp_client():
    """Test SMTP client initialization"""
    print("\n" + "="*60)
    print("4. TESTING SMTP CLIENT")
    print("="*60)
    
    errors = []
    
    try:
        from src.integrations.smtp_client import SMTPClient
        
        config = {
            "host": "smtp.gmail.com",
            "port": 587,
            "username": "test@example.com",
            "password": "test_password",
            "use_tls": True,
            "from_email": "test@example.com"
        }
        
        client = SMTPClient(config)
        print("✅ SMTPClient initialized successfully")
        
        # Test validation
        if client.validate_config():
            print("✅ SMTPClient config validation works")
        else:
            errors.append("❌ SMTPClient config validation failed")
            print("❌ SMTPClient config validation failed")
            
    except Exception as e:
        errors.append(f"❌ SMTP client test: {e}")
        print(f"❌ SMTP client test failed: {e}")
    
    return errors


def test_sendgrid_client():
    """Test SendGrid client initialization"""
    print("\n" + "="*60)
    print("5. TESTING SENDGRID CLIENT")
    print("="*60)
    
    errors = []
    
    try:
        from src.integrations.sendgrid_client import SendGridClient
        
        config = {
            "api_key": "SG.test_key_123",
            "from_email": "test@example.com",
            "from_name": "Test Sender"
        }
        
        client = SendGridClient(config)
        print("✅ SendGridClient initialized successfully")
        
        # Test validation
        if client.validate_config():
            print("✅ SendGridClient config validation works")
        else:
            errors.append("❌ SendGridClient config validation failed")
            print("❌ SendGridClient config validation failed")
            
    except Exception as e:
        errors.append(f"❌ SendGrid client test: {e}")
        print(f"❌ SendGrid client test failed: {e}")
    
    return errors


def test_client_supabase():
    """Test Client Supabase client initialization"""
    print("\n" + "="*60)
    print("6. TESTING CLIENT SUPABASE CLIENT")
    print("="*60)
    
    errors = []
    
    try:
        from src.integrations.client_supabase import ClientSupabaseClient
        
        config = {
            "supabase_url": "https://test.supabase.co",
            "supabase_key": "test_key_123",
            "allowed_tables": ["leads", "contacts"]
        }
        
        client = ClientSupabaseClient(config)
        print("✅ ClientSupabaseClient initialized successfully")
        
        # Test validation
        if client.validate_config():
            print("✅ ClientSupabaseClient config validation works")
        else:
            errors.append("❌ ClientSupabaseClient config validation failed")
            print("❌ ClientSupabaseClient config validation failed")
            
    except Exception as e:
        errors.append(f"❌ Client Supabase test: {e}")
        print(f"❌ Client Supabase test failed: {e}")
    
    return errors


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SPRINT 07A - VALIDAÇÃO PARCIAL")
    print("Testando tudo exceto Uazapi (aguardando documentação)")
    print("="*60)
    
    all_errors = []
    
    # Run tests
    all_errors.extend(test_imports())
    all_errors.extend(test_encryption())
    all_errors.extend(test_trigger_evaluator())
    all_errors.extend(test_smtp_client())
    all_errors.extend(test_sendgrid_client())
    all_errors.extend(test_client_supabase())
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if all_errors:
        print(f"\n❌ {len(all_errors)} errors found:\n")
        for error in all_errors:
            print(f"  {error}")
        print("\n⚠️  Some tests failed, but this is expected if .env is not configured")
        return 1
    else:
        print("\n✅ All tests passed!")
        print("\n📋 Next steps:")
        print("  1. Complete Uazapi documentation transcription")
        print("  2. Implement remaining Uazapi methods")
        print("  3. Run full validation: python validate_sprint07a.py")
        print("  4. Configure VPS: bash setup_vps_celery.sh")
        print("  5. Start frontend integration")
        return 0


if __name__ == "__main__":
    sys.exit(main())
