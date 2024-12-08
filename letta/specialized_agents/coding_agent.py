from typing import Dict, Any, Optional
import os
from letta.schemas.memory import ChatMemory
from letta.schemas.llm_config import LLMConfig

class CodingAgent:
    def __init__(self, client, shared_block, model_config: Optional[LLMConfig] = None):
        self.client = client
        self.shared_block = shared_block
        
        # Use DeepSeek configuration
        self.deepseek_config = {
            'api_key': os.getenv('DEEPSEEK_API_KEY'),
            'api_base': os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com/v1')
        }
        
        self.agent_state = self.client.create_agent(
            name="coding_agent",
            memory=ChatMemory(
                human="",
                persona=self._get_coding_persona()
            ),
            llm_config=model_config or self._get_default_config()
        )

    def _get_coding_persona(self) -> str:
        return """You are an expert coding agent specialized in implementing solutions based on research findings.
        Your responsibilities:
        1. Analyze research findings and requirements
        2. Implement code solutions using DeepSeek's advanced capabilities
        3. Follow best practices and coding standards
        4. Ensure code quality and maintainability
        5. Document code implementations
        6. Provide code explanations
        7. Suggest optimizations"""

    def _get_default_config(self) -> LLMConfig:
        return LLMConfig(
            model="deepseek-coder",
            api_key=self.deepseek_config['api_key'],
            api_base=self.deepseek_config['api_base'],
            temperature=0.2,
            max_tokens=2000
        )

    async def implement(self, research_findings: Dict[str, Any], request: str) -> Dict[str, Any]:
        # Analyze research findings and create implementation plan
        plan_prompt = f"""Based on these research findings and request, create an implementation plan:
        Research: {research_findings}
        Request: {request}
        """
        implementation_plan = await self.agent_state.aask(plan_prompt)
        
        # Generate code implementation
        code_prompt = f"""Following this implementation plan, generate the code:
        Plan: {implementation_plan}
        """
        code_implementation = await self.agent_state.aask(code_prompt)
        
        # Document the implementation
        documentation = await self._generate_documentation(implementation_plan, code_implementation)
        
        return {
            "plan": implementation_plan,
            "code": code_implementation,
            "documentation": documentation
        }

    async def _generate_documentation(self, plan: str, code: str) -> str:
        doc_prompt = f"""Please create comprehensive documentation for this implementation:
        Plan: {plan}
        Code: {code}
        """
        return await self.agent_state.aask(doc_prompt)
