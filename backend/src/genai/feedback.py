from datetime import datetime
from typing import Dict, Optional, List
from pydantic import BaseModel

class InterventionFeedback(BaseModel):
    intervention_id: str
    user_id: str
    rating: int # 1-5
    status: str # implemented, rejected, pending
    post_intervention_cluster_growth: Optional[float] = None
    timestamp: datetime = datetime.utcnow()

class FeedbackLoop:
    _db = [] # Stub for DB

    def submit_feedback(self, feedback: InterventionFeedback):
        self._db.append(feedback)
        
    def get_feedback_history(self, intervention_type: str = None) -> List[InterventionFeedback]:
        return self._db

    def calculate_effectiveness_score(self, intervention_id: str) -> float:
        # Aggregate ratings and outcome data
        feedbacks = [f for f in self._db if f.intervention_id == intervention_id]
        if not feedbacks:
            return 0.5 # Neutral start
            
        avg_rating = sum(f.rating for f in feedbacks) / len(feedbacks)
        return avg_rating / 5.0
