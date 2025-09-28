memory_store = []

def save_task(task: str, result):
    memory_store.append({"task": task, "result": result})

def get_memory():
    return memory_store
