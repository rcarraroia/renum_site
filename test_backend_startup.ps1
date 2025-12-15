$env:SUPABASE_URL = "https://grmwexchkfuztjikxtlp.supabase.co"
$env:SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdybXdleGNoa2Z1enRqaWt4dGxwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE5NzQwMTksImV4cCI6MjA0NzU1MDAxOX0.yXqVYgPgxQmhrKvslOGMQPJcPlhgMQV78kK4_MAWG40"
$env:SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdybXdleGNoa2Z1enRqaWt4dGxwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczMTk3NDAxOSwiZXhwIjoyMDQ3NTUwMDE5fQ.1YOHcY46xUo87_bwi8xrWHKL7tE7v_BQcGDCCGLMgEI"
$env:SECRET_KEY = "dummy_secret_key_for_testing"
$env:SUPABASE_JWT_SECRET = "dummy_jwt_secret_for_testing"
$env:CORS_ORIGINS = "http://localhost:5173,http://localhost:8000"
$env:OPENAI_API_KEY = "sk-dummy-openai-key-for-testing-structure"
$env:LANGSMITH_API_KEY = "lsv2-dummy-langsmith-key"
$env:PYTHONPATH = "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend"

Write-Host "Starting Backend with Test Credentials..."
& "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend\venv\Scripts\python.exe" -m uvicorn src.main:app --app-dir backend --host 127.0.0.1 --port 8000
