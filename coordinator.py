from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
from research_agents.query_agent import query_agent, QueryResponse
from research_agents.search_agent import search_agent
from research_agents.synthesis_agent import synthesis_agent
from ddgs import DDGS


class ResearchCoordinator:
    """
    A structured coordinator that ensures all research tools are used in sequence
    to generate comprehensive reports.
    """
    
    def __init__(self):
        self.ddgs = DDGS()
    
    async def generate_queries(self, topic: str) -> QueryResponse:
        """Generate focused search queries for the topic"""
        result = await Runner.run(query_agent, topic)
        return result.final_output
    
    def web_search(self, query: str, max_results: int = 3) -> list[dict]:
        """Search the web for the query and return results"""
        try:
            results = list(self.ddgs.text(
                query, 
                region="us-en", 
                safesearch="off", 
                timelimit="y", 
                max_results=max_results
            ))
            simplified = []
            for r in results:
                url = r.get("href") or r.get("url") or ""
                title = r.get("title") or "Untitled"
                if url:
                    simplified.append({"title": title, "url": url})
            return simplified
        except Exception as e:
            print(f"Web search failed for query '{query}': {e}")
            return []
    
    async def analyze_source(self, title: str, url: str) -> str:
        """Analyze the content at the URL and return a summary"""
        try:
            search_input = f"Title: {title}\nURL: {url}"
            result = await Runner.run(search_agent, input=search_input)
            return result.final_output or f"Failed to analyze {title}"
        except Exception as e:
            print(f"Source analysis failed for {url}: {e}")
            return f"Failed to analyze {title}: {e}"
    
    async def synthesize_report(self, original_query: str, sources_with_summaries: str) -> str:
        """Create a comprehensive report using all collected information"""
        try:
            findings_text = f"Query: {original_query}\n\nSearch Results:\n{sources_with_summaries}"
            result = Runner.run_streamed(synthesis_agent, input=findings_text)
            full_output = ""
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    output = event.data.delta
                    if output:
                        full_output += output
            return full_output or "Failed to generate report"
        except Exception as e:
            print(f"Report synthesis failed: {e}")
            return f"Failed to generate report: {e}"
    
    async def conduct_research_streaming(self, topic: str):
        """
        Conduct comprehensive research with streaming progress updates.
        Yields progress messages that can be streamed in Chainlit.
        """
        yield "🚀 Starting research...\n\n"
        
        # Step 1: Generate focused queries
        yield "🔍 Step 1: Generating search queries...\n"
        query_result = await self.generate_queries(topic)
        queries = query_result.queries
        thoughts = query_result.thoughts
        yield f"✅ Generated {len(queries)} queries\n"
        yield f"**Queries:** {', '.join(queries)}\n"
        yield f"**Strategy:** {thoughts}\n\n"
        
        # Step 2: Search for sources for each query
        yield "🌐 Step 2: Searching for sources...\n"
        all_sources = []
        for i, query in enumerate(queries):
            yield f"  Searching query {i+1}: {query[:50]}...\n"
            sources = self.web_search(query, max_results=2)
            all_sources.extend(sources)
            yield f"    Found {len(sources)} sources\n"
        
        # Remove duplicates based on URL
        unique_sources = []
        seen_urls = set()
        for source in all_sources:
            if source['url'] not in seen_urls:
                unique_sources.append(source)
                seen_urls.add(source['url'])
        
        yield f"✅ Found {len(unique_sources)} unique sources\n\n"
        
        # Step 3: Analyze each source
        yield "📖 Step 3: Analyzing sources...\n"
        source_summaries = []
        for i, source in enumerate(unique_sources):
            yield f"  Analyzing source {i+1}/{len(unique_sources)}: {source['title'][:50]}...\n"
            summary = await self.analyze_source(source['title'], source['url'])
            source_summaries.append(f"## {source['title']}\n**URL:** {source['url']}\n\n{summary}\n")
            yield f"    ✅ Analyzed: {source['title'][:50]}...\n"
        
        yield f"✅ Analyzed {len(unique_sources)} sources\n\n"
        
        # Step 4: Synthesize the final report
        yield "📝 Step 4: Synthesizing final report...\n"
        sources_text = "\n".join(source_summaries)
        final_report = await self.synthesize_report(topic, sources_text)
        
        yield "🎉 Research completed successfully!\n\n"
        yield f"# 📊 Research Report\n\n**Topic:** {topic}\n\n---\n\n{final_report}"

