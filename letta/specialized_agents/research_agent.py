import os
from typing import Dict, Any, Optional
from datetime import datetime
import json
from langchain_community.tools import TavilySearchResults
from letta.schemas.memory import ChatMemory
from letta.schemas.llm_config import LLMConfig

class ResearchAgent:
    def __init__(self, client, shared_block, enhanced_features: Optional[Dict[str, bool]] = None):
        self.client = client
        self.shared_block = shared_block
        self.search_tool = TavilySearchResults(
            api_key=os.getenv("TAVILY_API_KEY"),
            search_depth="advanced",
            include_domains=[
                "github.com",
                "stackoverflow.com",
                "python.org",
                "docs.python.org",
                "developer.mozilla.org"
            ]
        )
        
        # Initialize agent with shared memory
        self.agent_state = self.client.create_agent(
            name="research_agent",
            memory=ChatMemory(
                human="",
                persona=self._get_research_persona()
            ),
            tools=[self.search_tool.name]
        )

    def _get_research_persona(self) -> str:
        return """You are an advanced research agent specialized in technical research and documentation.
        Your responsibilities:
        1. Search and analyze programming topics
        2. Maintain comprehensive documentation
        3. Store and retrieve best practices
        4. Build knowledge base
        5. Track technology trends
        6. Share findings through shared memory
        7. Validate and update stored information"""

    async def research(self, query: str) -> Dict[str, Any]:
        # Use the search tool to gather information
        search_results = await self.search_tool.arun(query)
        
        # Process and structure the findings
        findings = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "results": search_results,
            "summary": await self._generate_summary(search_results)
        }
        
        # Store in shared memory
        self.shared_block.update({
            f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}": findings
        })
        
        return findings

    async def _generate_summary(self, search_results: list) -> str:
        # Ask the agent to generate a summary of findings
        summary_prompt = f"Please analyze these search results and provide a concise summary:\n{json.dumps(search_results, indent=2)}"
        response = await self.agent_state.aask(summary_prompt)
        return response
