from google.adk.tools import FunctionTool
from google.adk.tools import google_search # We import the built-in search tool here

# --- Custom Internal Tool (Used by SynthesizerAgent) ---
@FunctionTool
def synthesize_findings(research_data: str) -> str:
    """
    Synthesizes and formats the collected research data into a final report structure.
    This function should be called after all research is complete.
    """
    # NOTE: The LLM's instruction will use the text provided to 'research_data' 
    # to create the final report's structure and content.
    return f"Research data received and ready for final report generation: {research_data}"

# Placeholder for a Day 2 Best Practice Tool (HITL)
# @FunctionTool
# def trigger_human_approval(report_draft: str) -> str:
#     """
#     Triggers a Long-Running Operation that pauses the agent and requires a human
#     to review and approve the final report before it is published.
#     """
#     # In Day 2b, the body of this function would contain the logic to signal
#     # the ADK runner to pause and wait for external confirmation.
#     return "Approval request submitted. Waiting for human sign-off."

# List of all available tools
AVAILABLE_TOOLS = [
    google_search,
    synthesize_findings
    # trigger_human_approval,
]
