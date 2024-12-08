import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from letta.schemas.block import Block
from letta.schemas.memory import ChatMemory
from letta.schemas.llm_config import LLMConfig
from .research_agent import ResearchAgent
from .coding_agent import CodingAgent
from .memory_optimizer import MemoryOptimizer

class EnhancedOrchestratorAgent:
    """Advanced orchestrator with sophisticated agent coordination using DeepSeek"""
    def __init__(self):
        self.client = create_client()
        
        # DeepSeek Configuration
        self.deepseek_config = LLMConfig(
            model="deepseek-coder",
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            api_base=os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com/v1'),
            temperature=0.2,
            max_tokens=2000
        )
        
        # Create organization block
        self.org_block = Block(
            name="organization",
            value=json.dumps({
                "name": "LettaOS Technical Organization",
                "purpose": "Advanced technical research and implementation",
                "core_capabilities": [
                    "Research and Development",
                    "Code Implementation with DeepSeek",
                    "Documentation Management",
                    "Knowledge Optimization"
                ]
            })
        )
        
        # Initialize shared memory with organization context
        self.memory = ChatMemory(
            human="",
            persona=self._get_orchestrator_persona()
        )
        
        # Initialize agents with shared context and DeepSeek configuration
        self.research_agent = self._create_research_agent()
        self.coding_agent = self._create_coding_agent()
        
        # Initialize memory optimization
        self.memory_optimizer = MemoryOptimizer(self.client, self.org_block.id)

    def _get_orchestrator_persona(self) -> str:
        return """You are an advanced orchestrator agent responsible for:
1. Coordinating between research and coding agents
2. Managing shared knowledge and memory optimization
3. Ensuring efficient information flow between agents
4. Maintaining system-wide best practices
5. Optimizing resource utilization
6. Monitoring agent performance
7. Facilitating collaborative problem-solving"""

    def _create_research_agent(self) -> ResearchAgent:
        """Create and configure the research agent"""
        return ResearchAgent(
            client=self.client,
            shared_block=self.org_block,
            enhanced_features={"documentation_storage": True}
        )

    def _create_coding_agent(self) -> CodingAgent:
        """Create and configure the coding agent"""
        return CodingAgent(
            client=self.client,
            shared_block=self.org_block,
            llm_config=self.deepseek_config
        )

    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a complete task from research to implementation"""
        task_id = str(uuid.uuid4())
        task_context = self._create_task_context(task)
        
        try:
            # Phase 1: Research
            research_findings = await self.research_agent.research(task["query"])
            
            # Phase 2: Implementation Planning
            implementation_result = await self.coding_agent.implement(
                research_findings,
                task["requirements"]
            )
            
            # Phase 3: Memory Optimization
            await self.memory_optimizer.optimize_memory()
            
            # Phase 4: Result Compilation
            result = self._compile_task_result(
                task_id,
                task_context,
                research_findings,
                implementation_result
            )
            
            return result
            
        except Exception as e:
            return self._handle_task_error(task_id, str(e))

    def _create_task_context(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create context for a new task"""
        return {
            "timestamp": datetime.now().isoformat(),
            "task_type": task.get("type", "general"),
            "priority": task.get("priority", "medium"),
            "context": task.get("context", {}),
            "metadata": {
                "source": task.get("source", "user"),
                "domain": task.get("domain", "general")
            }
        }

    def _compile_task_result(
        self,
        task_id: str,
        context: Dict[str, Any],
        research: Dict[str, Any],
        implementation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compile the final task result"""
        return {
            "task_id": task_id,
            "status": "completed",
            "context": context,
            "research_findings": research,
            "implementation": implementation,
            "completion_time": datetime.now().isoformat()
        }

    def _handle_task_error(self, task_id: str, error_message: str) -> Dict[str, Any]:
        """Handle and format task errors"""
        return {
            "task_id": task_id,
            "status": "failed",
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        }
