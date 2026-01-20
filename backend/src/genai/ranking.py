from typing import List, Dict
from .feedback import FeedbackLoop

class MultiCriteriaRanker:
    def __init__(self):
        self.feedback_loop = FeedbackLoop()

    def rank_interventions(self, interventions: List[Dict]) -> List[Dict]:
        """
        Rank interventions based on Impact, Cost, Risk, and Feedback.
        """
        ranked = []
        for iv in interventions:
            # 1. Base Impact Score (from Causal Engine)
            impact = iv.get('predicted_impact', 0)
            
            # 2. Cost Estimate (Inverse)
            cost = iv.get('estimated_cost', 1000)
            cost_score = 1.0 / (cost + 1)
            
            # 3. Political Risk (Inverse)
            risk = iv.get('political_risk', 0.5) 
            risk_score = 1 - risk
            
            # 4. Historical Feedback
            feedback_score = 0.5 # Default
            if 'id' in iv:
                feedback_score = self.feedback_loop.calculate_effectiveness_score(iv['id'])
            
            # Composite Score
            final_score = (impact * 0.4) + (cost_score * 0.2) + (risk_score * 0.1) + (feedback_score * 0.3)
            
            iv['rank_score'] = final_score
            ranked.append(iv)
            
        return sorted(ranked, key=lambda x: x['rank_score'], reverse=True)
