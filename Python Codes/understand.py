import numpy as np
import pickle
import sys
import json
from typing import List, Tuple

class KNNFingerprintMatcher:
    def __init__(self):
        # KNN matching parameters
        self.min_matches = 4          # Reduced minimum matches
        self.lowes_ratio = 0.75        # More lenient ratio
        self.knn_k = 2                 # Standard KNN with k=2
        
        # Score calculation weights (fixed-point representation scaled by 100)
        self.distance_weight = 40      # 0.4 * 100
        self.count_weight = 60         # 0.6 * 100

    def load_features(self, feature_file):
        """Load features from file"""
        try:
            with open(feature_file, 'rb') as f:
                data = pickle.load(f)
                if not all(key in data for key in ['keypoints', 'descriptors']):
                    raise ValueError("Invalid feature file format")
                return data
        except Exception as e:
            print(f"Error loading features: {str(e)}")
            sys.exit(1)

    def bitwise_xor(self, a: np.uint8, b: np.uint8) -> np.uint8:
        """Implement bitwise XOR at the byte level"""
        
        return a ^ b

    def count_set_bits(self, x: np.uint8) -> int:
        """Count the number of set bits in a byte (Hamming weight)"""
        count = 0
        while x > 0:
            count += x & 1
            x >>= 1
        return count

    def hamming_distance(self, desc1: np.ndarray, desc2: np.ndarray) -> int:
        """Compute Hamming distance between two descriptors"""
        total_distance = 0
        for a, b in zip(desc1, desc2):
            xor_result = self.bitwise_xor(a, b)
            total_distance += self.count_set_bits(xor_result)
        return total_distance

    def knn_match_impl(self, query_descriptors: np.ndarray, train_descriptors: np.ndarray, k: int) -> List[List[Tuple[int, float]]]:
        """Complete KNN matching implementation"""
        matches = []
        
        for q_idx, q_desc in enumerate(query_descriptors):
            # Compute distances to all train descriptors
            distances = []
            for t_idx, t_desc in enumerate(train_descriptors):
                dist = self.hamming_distance(q_desc, t_desc)
                distances.append((t_idx, dist))
            
            # Sort by distance and keep top k
            distances.sort(key=lambda x: x[1])
            top_k = distances[:k]
            
            # Convert to match format (index, distance)
            matches.append([(idx, float(dist)) for idx, dist in top_k])
        
        print(matches)
        return matches

    def ratio_test(self, matches: List[List[Tuple[int, float]]]) -> List[Tuple[int, int, float]]:
        """Apply Lowe's ratio test to filter matches"""
        good_matches = []
        des_indx = 0
        for m in matches:
            if len(m) < 2:
                continue  # Not enough matches for ratio test
                
            best_match, second_best_match = m[0], m[1]
            ratio = best_match[1] / second_best_match[1]


            if ratio < self.lowes_ratio:
                good_matches.append((best_match[0], best_match[1]))
                print("Query Descriptor: ", des_indx, "Match")
            else:
                print("Query Descriptor: ", des_indx, "No Match")
            des_indx = des_indx + 1
        return good_matches

    def match(self, features1, features2, r1, r2):
        """Complete matching implementation with all components"""
        try:
            # Convert descriptors to numpy arrays
            des1_buffer = np.array(features1['descriptors'], dtype=np.uint8)
            des2_buffer = np.array(features2['descriptors'], dtype=np.uint8)
            np.set_printoptions(threshold=np.inf)

            #n = 3  # take only first n descriptors from both the files
            des1 = des1_buffer[:r1]
            des2 = des2_buffer[:r2]

            print("Number of rows in desc1_buffer:",des1_buffer.shape[0])
            print("Number of rows in desc1_buffer:",des2_buffer.shape[0])

            #sys.exit(1)

            # Early termination if not enough descriptors
            if len(des1) < self.knn_k or len(des2) < self.knn_k:
                return False, 0, 0, [], []
	
            # Perform complete matching pipeline
            raw_matches = self.knn_match_impl(des1, des2, self.knn_k)
            good_matches = self.ratio_test(raw_matches)
            num_good = len(good_matches)
            
            # Prepare match distances for output
            match_distances = []
            for m in raw_matches:
                if len(m) >= 2:
                    match_distances.append([m[0][1], m[1][1]])
                elif len(m) == 1:
                    match_distances.append([m[0][1], float('inf')])
            
            # Fixed-point scoring (scaled by 100)
            print("no. of good matches:",num_good)

            if num_good > 0:
                avg_distance = np.mean([dist for _, dist in good_matches])
                print("avg_distance:",avg_distance)

                normalized_quality = int(round((1 - (avg_distance / 256)) * 100))
                print("normalized avg distance:",normalized_quality)
                count_score = int(round(min(100, num_good / 30 * 100)))
                print("normalized match count:",count_score)
                final_score = (self.distance_weight * normalized_quality + 
                             self.count_weight * count_score) // 100
            else:
                final_score = 0

            print("Final Score:",final_score)

            # Match decision
            is_match = num_good >= self.min_matches

            return is_match, final_score, num_good, good_matches, match_distances
            
        except Exception as e:
            print(f"Matching error: {str(e)}")
            return False, 0, 0, [], []

    # ... (rest of the class methods remain the same) ...

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python knn_fingerprint_matcher.py features1.pkl features2.pkl r1 r2")
        sys.exit(1)

    matcher = KNNFingerprintMatcher()
    
    try:
        features1 = matcher.load_features(sys.argv[1])
        features2 = matcher.load_features(sys.argv[2])
        r1 = int(sys.argv[3])
        r2 = int(sys.argv[4])

        # Human-readable output
        is_match, score, num_matches, _, _ = matcher.match(features1, features2, r1, r2)
        print("\n=== Final Result ===")
        if is_match:
            print(f"✅ MATCH: Same fingerprint (score: {score}/100)")
        else:
            print(f"❌ NO MATCH: Different fingerprints")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
