
import json
import glob
import os

def check_latest_backup(prefix):
    files = glob.glob(f"{prefix}_*.json")
    if not files:
        print(f"❌ No backup found for {prefix}")
        return
    
    # Get latest file
    latest_file = max(files, key=os.path.getctime)
    
    try:
        with open(latest_file, "r", encoding='utf-8') as f:
            data = json.load(f)
            count = len(data)
            print(f"✓ {latest_file}: {count} records")
            
            if count > 0:
                keys = list(data[0].keys())
                print(f"  Fields verified: {', '.join(keys[:5])}...")
            else:
                print("  (Empty table)")
                
    except Exception as e:
        print(f"❌ Error reading {latest_file}: {e}")

print("--- VERIFICANDO ARQUIVOS DE BACKUP ---")
check_latest_backup("backup_renus_config")
check_latest_backup("backup_sub_agents")
check_latest_backup("backup_isa_commands")
