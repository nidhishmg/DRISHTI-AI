import json
from openai import OpenAI
from typing import Dict, Any
from ..config.settings import get_settings

settings = get_settings()

class InterventionGenerator:
    def __init__(self):
        # Stub: In real prod, this client should be resilient and have rate limits
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None

    def generate_intervention(self, archetype: Dict, cluster_summary: str) -> Dict[str, Any]:
        """
        Generate structured intervention plan using LLM.
        """
        if not self.client:
            return {"error": "LLM client not configured"}

        prompt = f"""
        Analyze this failure archetype:
        Title: {archetype.get('title')}
        Description: {archetype.get('description')}
        Cluster Summary: {cluster_summary}
        
        Generate a Govt-Standard Intervention Plan JSON with:
        - title
        - steps (list of actionable items)
        - estimated_cost (in INR, estimate)
        - expected_beneficiaries (count estimate)
        - assumptions
        - confidence_score (0-1)
        
        Output valid JSON only.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a Senior Policy Advisor specialized in Indian Govt Welfare Schemes."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
