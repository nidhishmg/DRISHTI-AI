from typing import List, Dict
import numpy as np
import math

class ActiveLearningSampler:
    def __init__(self):
        pass

    def sample_for_labeling(self, 
                          candidates: List[Dict], 
                          batch_size: int = 20) -> List[Dict]:
        """
        Select samples that are most ambiguous or informative.
        Strategies:
        1. Least Confidence (NER/Cluster)
        2. Entropy Sampling
        3. Drifted Samples
        """
        scored_candidates = []
        
        for item in candidates:
            # 1. NER Confidence (if available)
            ner_conf = item.get('ner_confidence', 1.0)
            
            # 2. Cluster Distance (if available) - Boundary points are important
            # lower probability = boundary point
            cluster_prob = item.get('cluster_probability', 1.0)
            
            # Combine scores (lower is more uncertain)
            uncertainty_score = 1 - (ner_conf * cluster_prob)
            
            item['uncertainty_score'] = uncertainty_score
            scored_candidates.append(item)
            
        # Sort by uncertainty (highest first)
        scored_candidates.sort(key=lambda x: x['uncertainty_score'], reverse=True)
        
        return scored_candidates[:batch_size]
