from agents import Agent, function_tool, Runner
from config import agent_model
from research_agents.query_agent import query_agent, QueryResponse
from research_agents.search_agent import search_agent
from research_agents.synthesis_agent import synthesis_agent
from ddgs import DDGS
import json


@function_tool
async def generate_queries(topic: str) -> str:
    """
    Generate focused search queries and research plan for the topic.
    Returns JSON with: {"queries": string[], "thoughts": string}
    """
    result = await Runner.run(query_agent, topic)
    final: QueryResponse = result.final_output
    # return json.dumps({"queries": final.queries, "thoughts": final.thoughts})
    return f"Queries: {final.queries}\nThoughts: {final.thoughts}"


@function_tool
def web_search(query: str, max_results: int = 1) -> str:
    """
    Search the web for the query and return a JSON list of results.
    Each result: {"title": str, "url": str}
    """
    try:
        results = list(DDGS().text(query, region="us-en", safesearch="off", timelimit="y", max_results=max_results))
        simplified = []
        for r in results:
            url = r.get("href") or r.get("url") or ""
            title = r.get("title") or "Untitled"
            if url:
                simplified.append({"title": title, "url": url})
        # return json.dumps(simplified)
        return simplified
    except Exception as e:
        # return json.dumps({"error": f"web_search failed: {e}"})
        return f"Web Search failed: {e}"


@function_tool
async def analyze_source(title: str, url: str) -> str:
    """
    Analyze the content at the URL and return a concise summary (2-3 paragraphs).
    """
    search_input = f"Title: {title}\nURL: {url}"
    result = await Runner.run(search_agent, input=search_input)
    return result.final_output or ""


@function_tool
async def synthesize_report(original_query: str, sources_with_summaries: str) -> str:
    """
    Create a comprehensive markdown report for the original_query using sources_with_summaries.
    sources_with_summaries should be a markdown or bullet list of citations and summaries.
    """
    findings_text = f"Query: {original_query}\n\nSearch Results:\n{sources_with_summaries}"
    result = await Runner.run(synthesis_agent, input=findings_text)
    return result.final_output or ""


RESEARCH_INSTRUCTIONS = (
    "You are a comprehensive research orchestrator. You MUST follow this EXACT sequence:\n\n"
    "STEP 1: Use generate_queries(topic) to create focused 3 search queries\n"
    "STEP 2: For each query from step 1, use web_search(query) to find relevant sources\n"
    "STEP 3: For each promising source found, use analyze_source(title, url) to extract summaries\n"
    "STEP 4: Collect all summaries and use synthesize_report(original_query, sources_with_summaries) to create the final report\n\n"
    "IMPORTANT: You MUST complete ALL 4 steps in order. Do not skip any step. "
    "The final output should be the comprehensive report from synthesize_report. "
    "Be thorough and systematic in your research process."
)


research_agent = Agent(
    name="Research Agent",
    instructions=RESEARCH_INSTRUCTIONS,
    tools=[generate_queries, web_search, analyze_source, synthesize_report],
    model=agent_model,
)


