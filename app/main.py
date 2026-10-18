import os
import sys
import time

# Ensure the repository root is importable when this file is run directly.
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from app.tools import CodebaseSandbox
from app.agent import SentinelAgent

def main():
    repo_path = os.path.join(os.path.dirname(current_dir), "demo_repo")
    sandbox = CodebaseSandbox(repo_path)
    agent = SentinelAgent(sandbox=sandbox, max_iterations=3)

    # Simulated Incoming Webhook payload from an APM / Sentry trigger
    simulated_incident = {
        "incident_id": "INC-20261018-0941",
        "timestamp": "2026-10-18T03:20:00Z",
        "service": "billing-pipeline",
        "error_type": "ZeroDivisionError & TypeError",
        "message": "float division by zero at process_batch_transactions:34 / unsupported operand type(s) for *: 'NoneType' and 'float'",
        "suspected_file": "metrics_engine.py"
    }

    print("\n" + "#"*70)
    print("      🚀 SENTINEL AGENT: AUTONOMOUS SRE & AUTO-HEALING ENGINE")
    print("      Omnirush Agentic Buildathon 2026 Submission")
    print("#"*70)

    time.sleep(1)
    result = agent.run(simulated_incident)

    print("\n" + "="*70)
    print("📋 [FINAL STATUS]:", result["status"])
    print("="*70)

    if result["status"] == "RESOLVED":
        pr = result["pr"]
        print(f"\n🎉 PULL REQUEST PAYLOAD GENERATED:")
        print(f"Title: {pr['title']}\n")
        print(pr["body"])
    elif result["status"] == "NO_ACTION_NEEDED":
        print("ℹ️ No action was needed; the target test suite is already passing.")
    else:
        print("❌ Could not resolve the issue within the iteration threshold.")

if __name__ == "__main__":
    main()
