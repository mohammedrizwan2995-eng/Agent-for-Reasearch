import json
from pydantic import BaseModel, Field
from google.genai import GenerativeModel, types

# --- 2.1 Pydantic Schema for Structured Output ---
# This ensures the Judge LLM returns a machine-readable, reliable score.
class EvaluationScore(BaseModel):
    """Schema for the LLM Judge to output the final score and justification."""
    score_pass_fail: str = Field(description="Must be 'PASS' or 'FAIL' based on meeting all criteria.")
    completeness_score: int = Field(description="Score from 1 to 5 on how completely the answer addressed the query (5 is perfect).")
    criteria_met: list[str] = Field(description="List all met criteria from the expected_criteria list.")
    justification: str = Field(description="A brief explanation of why the final score was given.")

# --- 2.2 The Judge Logic ---

def create_judge_prompt(query: str, agent_output: str, expected_criteria: list[str]) -> str:
    """Creates the detailed System Instruction for the Judge LLM."""
    criteria_list = "\n".join([f"- {c}" for c in expected_criteria])
    
    # This prompt establishes the Judge's persona and rules (Day 4b)
    prompt = f"""
    You are an impartial AI Judge specializing in assessing the performance of autonomous agents.
    Your task is to analyze the tested agent's output against the user's query and the specific criteria below.
    
    1. STRICTLY evaluate the output against ALL of the expected criteria.
    2. Assign 'PASS' only if ALL criteria are met. Otherwise, assign 'FAIL'.
    3. Use the provided JSON format for your response.

    ---
    ORIGINAL USER QUERY: {query}
    ---
    EXPECTED CRITERIA:
    {criteria_list}
    ---
    AGENT'S FINAL OUTPUT:
    {agent_output}
    """
    return prompt

async def run_llm_as_a_judge(query: str, agent_output: str, expected_criteria: list[str]) -> EvaluationScore:
    """Sends the agent's output to the Judge LLM for scoring."""
    
    judge_model = GenerativeModel(model='gemini-2.5-pro') # Use a high-quality model for judging
    
    judge_prompt = create_judge_prompt(query, agent_output, expected_criteria)
    
    # Use response schema to enforce the structured JSON output
    response_schema = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=EvaluationScore,
    )

    try:
        response = await judge_model.generate_content_async(
            contents=judge_prompt,
            config=response_schema
        )
        # Parse the structured JSON output into the Pydantic model
        score_data = json.loads(response.text)
        return EvaluationScore(**score_data)
        
    except Exception as e:
        print(f"Judge Model Error: {e}")
        return EvaluationScore(
            score_pass_fail="ERROR", 
            completeness_score=0, 
            criteria_met=[], 
            justification="Judge model failed to return a valid JSON format."
        )
