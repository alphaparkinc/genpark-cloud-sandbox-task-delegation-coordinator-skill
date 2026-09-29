import sys
import json
from client import CloudSandboxTaskCoordinator

coordinator = CloudSandboxTaskCoordinator()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-cloud-sandbox-task-delegation-coordinator-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "delegate_task",
                        "description": "Delegate a long-running research or browsing task to persistent cloud sandbox",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string"},
                                "title": {"type": "string"},
                                "estimated_duration_sec": {"type": "number"}
                            },
                            "required": ["task_id", "title"]
                        }
                    },
                    {
                        "name": "record_checkpoint",
                        "description": "Record intermediate progress and state checkpoint",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string"},
                                "step_name": {"type": "string"},
                                "progress_pct": {"type": "number"}
                            },
                            "required": ["task_id", "step_name", "progress_pct"]
                        }
                    },
                    {
                        "name": "complete_task",
                        "description": "Mark task completed and set final summary for delivery to user",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string"},
                                "result_summary": {"type": "string"}
                            },
                            "required": ["task_id", "result_summary"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "delegate_task":
            res = coordinator.delegate_task(args["task_id"], args["title"], args.get("estimated_duration_sec", 60))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tool_name == "record_checkpoint":
            res = coordinator.record_checkpoint(args["task_id"], args["step_name"], args["progress_pct"])
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tool_name == "complete_task":
            res = coordinator.complete_task(args["task_id"], args["result_summary"])
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
