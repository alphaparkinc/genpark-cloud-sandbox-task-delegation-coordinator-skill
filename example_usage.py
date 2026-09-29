from client import CloudSandboxTaskCoordinator

coordinator = CloudSandboxTaskCoordinator()

# Delegate a long-running research task to cloud sandbox
task = coordinator.delegate_task("TASK_AUDIT_99", "Deep Web Price Benchmark", estimated_duration_sec=45)
print("Delegated Task:", task["task_id"], task["status"])

# Save milestone checkpoint
coordinator.record_checkpoint("TASK_AUDIT_99", "Fetched 12 merchant APIs", progress_pct=50)

# Emit progress heartbeat for messaging chat UI
hb = coordinator.emit_heartbeat("TASK_AUDIT_99", "Synthesizing cross-merchant price table...")
print(f"Heartbeat: [{hb['progress']}%] {hb['message']}")

# Complete
completed = coordinator.complete_task("TASK_AUDIT_99", "Found lowest price: $24.99 at Target.")
print("Completion Summary:", completed["summary"])
