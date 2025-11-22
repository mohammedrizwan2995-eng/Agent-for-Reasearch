import asyncio
import json
import pytest
from google.adk.runners import InMemoryRunner
from agent_app.workflows import create_capstone_pipeline
from .evaluator import run_llm_as_a_judge

# --- Load Golden Data (Day 4b) ---
with open('evaluation/golden_data.json', 'r') as f:
    GOLDEN_DATA = json.load(f)

# --- Pytest Fixture ---
@pytest.fixture(scope="session")
def agent_runner():
    """A fixture to provide a single instance of the agent pipeline runner."""
    return InMemoryRunner(agent=create_capstone_pipeline())

# --- Test Cases ---
@pytest.mark.asyncio
@pytest.mark.parametrize("test_case", GOLDEN_DATA, ids=[data['id'] for data in GOLDEN_DATA])
async def test_capstone_agent_quality(agent_runner, test_case):
    """The main evaluation function that runs the agent and submits the output to the Judge LLM."""
    
    print(f"\n--- Running Test: {test_case['id']} ---")
    
    # 1. Execute the Agent (The target of the evaluation)
    # Note: run_debug is used here to get rich logs (Day 4a)
    agent_response = await agent_runner.run_debug(test_case['query'])
    
    agent_output = agent_response.message.text
    
    # 2. Run the LLM-as-a-Judge (The scoring mechanism)
    evaluation_result = await run_llm_as_a_judge(
        query=test_case['query'],
        agent_output=agent_output,
        expected_criteria=test_case['expected_criteria']
    )

    # 3. Assertion: This is the mandatory Evaluation Gate check (Day 5)
    print(f"\nJudge Score: {evaluation_result.score_pass_fail}")
    print(f"Justification: {evaluation_result.justification}")
    
    # Fail the test if the Judge determines the criteria were not met
    assert evaluation_result.score_pass_fail == "PASS", f"Evaluation Failed: {evaluation_result.justification}"
    
    # Also fail if the Judge couldn't parse the output correctly
    assert evaluation_result.score_pass_fail != "ERROR", "Evaluation Judge Error."


if __name__ == '__main__':
    # To run this file: pytest evaluation/test_agent.py --asyncio-mode=strict -s
    # In a CI/CD pipeline, the successful exit code from pytest (0) would trigger deployment.
    pytest.main(["evaluation/test_agent.py", "--asyncio-mode=strict", "-s"])
