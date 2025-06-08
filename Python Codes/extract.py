import numpy as np
import pickle
import sys
import json
from typing import List, Tuple

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python knn_fingerprint_matcher.py features1.pkl features2.pkl  r1 r2")
        sys.exit(1)
    try:
        # Convert NumPy arrays to binary string representations

        def to_binary_bit_lists(array, n2):
            return [[int(bit) for val in row[:n2] for bit in format(val, '08b')] for row in array.tolist()]

        r1 = int(sys.argv[3])  # take only first n descriptors from both the files
        r2 = int(sys.argv[4])

        with open(sys.argv[1], 'rb') as f:
                features1 = pickle.load(f)
                if not all(key in features1 for key in ['keypoints', 'descriptors']):
                    raise ValueError("Invalid feature file format")

        with open(sys.argv[2], 'rb') as f:
                features2 = pickle.load(f)
                if not all(key in features2 for key in ['keypoints', 'descriptors']):
                    raise ValueError("Invalid feature file format")

        
        des1_buffer = np.array(features1['descriptors'], dtype=np.uint8)
        des2_buffer = np.array(features2['descriptors'], dtype=np.uint8)
        des1 = des1_buffer[:r1]
        des2 = des2_buffer[:r2]
        

        binary_des1 = to_binary_bit_lists(des1, 32)
        binary_des2 = to_binary_bit_lists(des2, 32)

        output = {
                "debug": 0,
                "LRatio": 7500, #  0.85 *10000
                "max_matches": 30,
                "dist_weight": 40, # 0.4 * 100
                "match_cnt_threshold": 4,
                "in1": binary_des1,
                "in2": binary_des2
        }

        with open("input4.json", "w") as f:
                json.dump(output, f, indent=2)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)