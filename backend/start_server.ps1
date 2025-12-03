$env:PYTHONPATH = "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend"
Set-Location "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend"
& "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend\.venv\Scripts\python.exe" -m uvicorn src.main:app --host 0.0.0.0 --port 8000
