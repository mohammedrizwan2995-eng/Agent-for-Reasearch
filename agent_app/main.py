import os
import asyncio
from google.adk.runners import InMemoryRunner
from .workflows import create_capstone_pipeline

# --- Authentication Check ---
try:
    # NOTE: Assumes GOOGLE_API_KEY is set in your environment
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found.")
    print("✅ Authentication check passed.")
except Exception as e:
    print(f"🔑 Setup Error: {e}")
    
# --- Runner Execution (Day 4a - Observability) ---

async def main():
    """Instantiates and runs the Capstone Agent Pipeline."""
    
    # 1. Instantiate the Root Agent
    root_agent = create_capstone_pipeline()
    
    # 2. Define the Test Query
    query = "Create an executive briefing on the future of enterprise automation, covering Agentic AI, Quantum Computing, and deployment strategies."

    print(f"\n--- Starting Capstone Agent for Query: '{query}' ---")
    
    # 3. Run the Agent (Using the debug runner for internal visibility)
    runner = InMemoryRunner(agent=root_agent)
    
    # The run_debug method logs the full execution trace (Day 4a)
    response = await runner.run_debug(query) 
    
    print("\n--- FINAL REPORT ---")
    print(response.message.text)
    
    # Final Output Check
    if "Research data received" in response.message.text:
        print("\n✅ Success: Workflow ran and called the final synthesize_findings tool.")
    else:
        print("\n❌ Failure: Final step not executed correctly.")

if __name__ == "__main__":
    # Standard way to run the async main function
    asyncio.run(main())
