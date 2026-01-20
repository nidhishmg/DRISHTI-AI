import numpy as np
from scipy.spatial.distance import cosine
from scipy.stats import ks_2samp
from typing import List, Dict
from ..config.settings import get_settings

settings = get_settings()

class DriftDetector:
    def __init__(self, reference_embeddings: np.ndarray = None):
        self.reference_embeddings = reference_embeddings

    def set_reference(self, embeddings: np.ndarray):
        """
        Set baseline embeddings for drift detection.
        Usually from Training or previous week's data.
        """
        self.reference_embeddings = embeddings

    def detect_drift(self, new_embeddings: np.ndarray) -> Dict[str, Any]:
        """
        Detect if new batch of embeddings has drifted from reference.
        Uses Kolmogorov-Smirnov test on cosine distances to mean.
        """
        if self.reference_embeddings is None:
            return {"drift_detected": False, "reason": "No reference data"}
            
        # 1. Compute Centroids
        ref_centroid = np.mean(self.reference_embeddings, axis=0)
        new_centroid = np.mean(new_embeddings, axis=0)
        
        # 2. Compute Distances to *Reference* Centroid
        # (How far is point P from the 'Normal' center?)
        ref_dists = [cosine(e, ref_centroid) for e in self.reference_embeddings]
        new_dists = [cosine(e, ref_centroid) for e in new_embeddings]
        
        # 3. K-S Test on Distributions
        statistic, p_value = ks_2samp(ref_dists, new_dists)
        
        # 4. Check Thresholds
        is_drift = p_value < 0.05 and statistic > settings.DRIFT_THRESHOLD
        
        return {
            "drift_detected": is_drift,
            "p_value": p_value,
            "statistic": statistic,
            "centroid_shift": cosine(ref_centroid, new_centroid)
        }
