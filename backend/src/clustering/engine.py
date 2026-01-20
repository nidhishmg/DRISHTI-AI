import numpy as np
import pandas as pd
from typing import List, Dict, Any
# Lazy imports for heavy libs handled inside methods or class init
from ..core.model_registry import ModelRegistry
from ..config.settings import get_settings

class ClusterManager:
    def __init__(self):
        self.settings = get_settings()
        import umap
        import hdbscan

        
        # Initialize UMAP for dimension reduction
        self.reducer = umap.UMAP(
            n_neighbors=15,
            n_components=5,
            metric='cosine',
            random_state=42
        )
        
        # Initialize HDBSCAN for density-based clustering
        self.clusterer = hdbscan.HDBSCAN(
            min_cluster_size=5,
            min_samples=2,
            metric='euclidean',
            cluster_selection_method='eom',
            prediction_data=True
        )
        
        self.is_fitted = False

    def fit_transform(self, embeddings: np.ndarray) -> Dict[str, Any]:
        """
        Fit the clustering model on a batch of embeddings.
        Returns cluster labels and probabilities.
        """
        if len(embeddings) < 10:
             # Not enough data to cluster meaningfully
             return {"labels": [-1] * len(embeddings), "probs": [0.0] * len(embeddings)}

        # Optimization: Batch Limit
        if len(embeddings) > self.settings.CLUSTERING_BATCH_SIZE:
             # Trim for demo/performance (in production we'd chunk or sample)
             embeddings = embeddings[:self.settings.CLUSTERING_BATCH_SIZE]

        # Optimization: Incremental Mode
        if not self.settings.FULL_RECLUSTER and self.is_fitted:
             # Use prediction for speed instead of re-fitting everything
             # Note: This returns labels for the input batch based on existing structure
             try:
                 labels = []
                 probs = []
                 for emb in embeddings:
                     try:
                         l = self.predict(emb)
                         labels.append(l)
                         probs.append(0.8) # Mock prob for fast path
                     except Exception:
                         labels.append(-1)
                         probs.append(0.0)
                 return {
                     "labels": labels,
                     "probabilities": probs,
                     "reduced_data": [] # Skip reduction for speed/bandwidth
                 }
             except Exception as e:
                 print(f"Incremental prediction failed, falling back to full fit: {e}")
                 pass

        # 1. Reduce Dimensions

        reduced_data = self.reducer.fit_transform(embeddings)
        
        # 2. Cluster
        labels = self.clusterer.fit_predict(reduced_data)
        probabilities = self.clusterer.probabilities_
        
        self.is_fitted = True
        
        return {
            "labels": labels.tolist(),
            "probabilities": probabilities.tolist(),
            "reduced_data": reduced_data.tolist()
        }

    def predict(self, embedding: np.ndarray) -> int:
        """
        Predict cluster for a new single embedding.
        Requires model to be fitted.
        """
        import hdbscan
        
        if not self.is_fitted:
            raise ValueError("ClusterManager is not fitted yet.")
            
        # Transform using fitted reducer
        reduced_point = self.reducer.transform(embedding.reshape(1, -1))
        
        # Predict using fuzzy logic from HDBSCAN (using approximate_predict if available, else re-fit)
        # Note: approximate_predict requires all points_to_predict
        # For strict stream clustering, we might need a separate mechanism or online clustering
        # Here we assume soft-clustering assignment or nearest centroid for simplicity in phase 2A
        
        labels, strengths = hdbscan.approximate_predict(self.clusterer, reduced_point)
        return labels[0]
