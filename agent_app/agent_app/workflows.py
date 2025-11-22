from google.adk.agents import SequentialAgent, ParallelAgent, Agent
from .agents import create_planner_agent, create_synthesizer_agent, create_researcher_template_agent
from .tools import google_search # For explicit tool assignment

# --- The Workflow Composition (Day 1) ---

def create_capstone_pipeline() -> SequentialAgent:
    """
    Defines the full Sequential/Parallel Capstone Agent workflow.
    """
    
    # 1. Planner Agent (The First Step in the Sequence)
    planner_agent = create_planner_agent()
    
    # 2. Parallel Research Team (The Parallel Step)
    # NOTE: In an advanced capstone, these would be dynamically created based on the Planner's output.
    # Here, we hardcode 3 for demonstration.
    
    # Clone the researcher template and assign specific tasks
    topic1_researcher = Agent(
        name="Topic1_Researcher",
        model="gemini-2.5-flash-lite",
        instruction="Find 2-3 key findings on the **rise of Agentic AI** and its implications.",
        tools=[google_search],
        output_key="topic1_research"
    )
    topic2_researcher = Agent(
        name="Topic2_Researcher",
        model="gemini-2.5-flash-lite",
        instruction="Find 2-3 key findings on the **latest developments in Quantum Computing**.",
        tools=[google_search],
        output_key="topic2_research"
    )
    topic3_researcher = Agent(
        name="Topic3_Researcher",
        model="gemini-2.5-flash-lite",
        instruction="Find 2-3 key findings on **safe rollout strategies for large models** (Canary/Blue-Green).",
        tools=[google_search],
        output_key="topic3_research"
    )

    parallel_research_team = ParallelAgent(
        name="ParallelTopicResearch",
        sub_agents=[topic1_researcher, topic2_researcher, topic3_researcher],
    )
    
    # 3. Synthesizer Agent (The Final Step in the Sequence)
    synthesizer_agent = create_synthesizer_agent()
    
    # Combine all research outputs from the parallel step into a single context for the synthesizer
    synthesizer_with_context = synthesizer_agent.with_context(
        combined_research="""
        Findings on Agentic AI: {topic1_research}
        \n--- Findings on Quantum Computing: {topic2_research}
        \n--- Findings on Safe Rollout: {topic3_research}
        """
    )

    # Define the final, sequential pipeline
    root_agent = SequentialAgent(
        name="CapstoneResearchPipeline",
        sub_agents=[
            planner_agent,             # Step 1: Planning
            parallel_research_team,    # Step 2: Concurrent Execution
            synthesizer_with_context   # Step 3: Synthesis
        ]
    )
    return root_agent
