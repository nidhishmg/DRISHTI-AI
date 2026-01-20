import numpy as np

class CausalConfidenceIndex:
    @staticmethod
    def calculate(
        effect_size: float,
        p_value: float,
        placebo_effect: float,
        lag_stability_score: float
    ) -> float:
        """
        Calculate CCI score [0-1].
        """
        # 1. Significance: (1 - p_value) clamped
        sig_score = max(0.0, 1.0 - p_value)
        if p_value > 0.05:
            sig_score *= 0.5 # Penalize non-significant results heavily
            
        # 2. Robustness: Relative failure of placebo
        # Ideally, placebo effect should be 0.
        # If placebo effect is close to actual effect, robustness is low.
        if abs(effect_size) < 1e-9:
            robust_score = 0.0
        else:
            ratio = abs(placebo_effect / effect_size)
            robust_score = max(0.0, 1.0 - ratio)
            
        # 3. Stability
        stab_score = lag_stability_score
        
        # Weighted Aggregation
        # Weights: Significance(40%), Robustness(40%), Stability(20%)
        cci = (sig_score * 0.4) + (robust_score * 0.4) + (stab_score * 0.2)
        
        return round(cci, 3)
