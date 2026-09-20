import json
import os
import shutil
import time
from datetime import datetime

# CONFIGURATION
NERVE_CENTER_ROOT = r"C:\Users\casey\hermes-nerve-center"
INBOX = os.path.join(NERVE_CENTER_ROOT, "inbox")
PROCESSING = os.path.join(NERVE_CENTER_ROOT, "processing")
COMPLETED = os.path.join(NERVE_CENTER_ROOT, "completed")
FAILED = os.path.join(NERVE_CENTER_ROOT, "failed")
REGISTRY_FILE = os.path.join(NERVE_CENTER_ROOT, "registry.json")

def update_registry(task_id, status, progress="0%", error=None):
    registry = {"active_tasks": [], "last_error": None}
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, 'r') as f:
                registry = json.load(f)
        except:
            pass

    # Update or add task
    found = False
    for task in registry["active_tasks"]:
        if task["task_id"] == task_id:
            task["status"] = status
            task["progress"] = progress
            task["last_update"] = datetime.utcnow().isoformat()
            if error: task["error"] = error
            found = True
            break
    
    if not found and status != "COMPLETED" and status != "FAILED":
        registry["active_tasks"].append({
            "task_id": task_id,
            "status": status,
            "progress": progress,
            "last_update": datetime.utcnow().isoformat()
        })
    
    if status in ["COMPLETED", "FAILED"]:
        registry["active_tasks"] = [t for t in registry["active_tasks"] if t["task_id"] != task_id]
        if status == "FAILED":
            registry["last_error"] = error

    with open(REGISTRY_FILE, 'w') as f:
        json.dump(registry, f, indent=2)

def process_new_task(file_path):
    task_id = os.path.basename(file_path).replace(".json", "")
    print(f"[*] New signal detected: {task_id}")
    
    # Move to processing
    target_path = os.path.join(PROCESSING, os.path.basename(file_path))
    shutil.move(file_path, target_path)
    
    try:
        with open(target_path, 'r') as f:
            task_data = json.load(f)
        
        task_id = task_data.get("task_id", task_id)
        print(f"[*] Task {task_id} ingested. Category: {task_data.get('category')}")
        
        # Update registry to show we are working
        update_registry(task_id, "IN_PROGRESS", "1%")
        
        # In a real scenario, this is where Hermes would be triggered via a webhook or subprocess.
        # For this local script, we'll just simulate the "Handover" by printing a trigger command.
        print(f"\n[!!!] SIGNAL TO HERMES [!!!]")
        print(f"TASK_ID: {task_id}")
        print(f"INSTRUCTION: {task_data.get('instruction')}")
        print(f"CONTEXT: {json.dumps(task_data.get('context'))}")
        print(f"---------------------------\n")
        
        # For the sake of the demo script, we move it to completed immediately 
        # so the watchdog doesn't loop. In production, this is replaced by actual work.
        shutil.move(target_path, os.path.join(COMPLETED, os.path.basename(file_path)))
        update_registry(task_id, "COMPLETED", "100%")
        print(f"[+] Task {task_id} processed and archived.")

    except Exception as e:
        print(f"[!] Error processing task: {e}")
        shutil.move(target_path, os.path.join(FAILED, os.path.basename(file_path)))
        with open(os.path.join(FAILED, f"{task_id}_error.log"), 'w') as f:
            f.write(str(e))
        update_registry(task_id, "FAILED", error=str(e))

def run_watchdog():
    print(f"[*] Hermes Nerve Center Watchdog active on {INBOX}")
    print("[*] Press Ctrl+C to terminate.")
    
    # Ensure registry exists
    if not os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, 'w') as f:
            json.dump({"active_tasks": [], "last_error": None}, f)

    try:
        while True:
            files = [f for f in os.listdir(INBOX) if f.endswith(".json")]
            for f in files:
                process_new_task(os.path.join(INBOX, f))
            time.sleep(2) # Check every 2 seconds
    except KeyboardInterrupt:
        print("\n[*] Watchdog stopped by user.")

if __name__ == "__main__":
    run_watchdog()
