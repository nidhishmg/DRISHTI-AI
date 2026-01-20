from simhash import Simhash
from datasketch import MinHash
from typing import List, Union
import re

class FingerprintService:
    @staticmethod
    def get_features(text: str) -> List[str]:
        # Basic tokenization (width=3 shingles could be better but sticking to words for simhash)
        width = 3
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = text.split()
        return [tokens[i:i+width] for i in range(max(0, len(tokens)-width+1))]

    @staticmethod
    def compute_simhash(text: str) -> str:
        features = FingerprintService.get_features(text)
        return str(Simhash(features).value)

    @staticmethod
    def compute_minhash(text: str, num_perm: int = 128) -> List[int]:
        m = MinHash(num_perm=num_perm)
        features = set(text.lower().split()) # Standard bag of words for MinHash
        for f in features:
            m.update(f.encode('utf8'))
        return list(m.digest()) # Convert numpy array to list for JSON serialization

    @staticmethod
    def is_duplicate_simhash(hash1: str, hash2: str, threshold: int = 3) -> bool:
        """
        Returns True if hamming distance <= threshold.
        """
        h1 = int(hash1)
        h2 = int(hash2)
        x = (h1 ^ h2) & ((1 << 64) - 1)
        ans = 0
        while x:
            ans += 1
            x &= x - 1
        return ans <= threshold
