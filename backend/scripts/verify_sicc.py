import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Adiciona o diretório raiz ao PYTHONPATH para importar módulos src
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from src.config.supabase import supabase_admin

async def verify_sicc_data():
    """
    Verifica a existência de memórias, logs de aprendizado e padrões comportamentais.
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "renus_id": None,
        "memories": [],
        "learning_logs": [],
        "behavior_patterns": []
    }

    try:
        # 1. Obter ID do RENUS
        response = supabase_admin.table('agents').select('id').eq('name', 'RENUS').execute()
        if response.data:
            results["renus_id"] = response.data[0]['id']
            agent_id = results["renus_id"]
            
            # 2. Buscar Memórias (memory_chunks)
            # Assumindo tabela 'memory_chunks' e coluna 'agent_id'
            mem_response = supabase_admin.table('memory_chunks')\
                .select('*')\
                .eq('agent_id', agent_id)\
                .order('created_at', desc=True)\
                .limit(10)\
                .execute()
            results["memories"] = mem_response.data

            # 3. Buscar Logs de Aprendizado (learning_logs or logs?)
            # Assumindo tabela 'learning_logs' - verificar nome correto se falhar, mas logica indica logs
            # Pode ser learning_queue ou similar. Vamos tentar learning_logs
            try:
                log_response = supabase_admin.table('learning_logs')\
                    .select('*')\
                    .eq('agent_id', agent_id)\
                    .order('created_at', desc=True)\
                    .limit(10)\
                    .execute()
                results["learning_logs"] = log_response.data
            except Exception as e:
                results["learning_logs_error"] = str(e)

            # 4. Buscar Padrões Comportamentais (behavior_patterns)
            try:
                pat_response = supabase_admin.table('behavior_patterns')\
                    .select('*')\
                    .eq('agent_id', agent_id)\
                    .order('created_at', desc=True)\
                    .limit(5)\
                    .execute()
                results["behavior_patterns"] = pat_response.data
            except Exception as e:
                results["behavior_patterns_error"] = str(e)

        else:
            results["error"] = "RENUS agent not found"

    except Exception as e:
        results["global_error"] = str(e)

    # Imprimir resultado em JSON para fácil leitura
    print(json.dumps(results, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(verify_sicc_data())
