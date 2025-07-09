import numpy as np
import pickle
import sys
import json
from typing import List, Tuple


def read_params(path: str) -> dict:
    def convert(value: str):
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return value  # fallback to string if it's not a number

    params = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if '=' in line:
                    key, val = line.split('=', 1)
                    params[key.strip()] = convert(val.strip())
    return params




if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python knn_fingerprint_matcher.py Features1.pkl Features2.pkl  r1 r2")
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

        params = read_params("params.dat")

        debug = params.get("CircomDebug", 0)  # 0 is default if key is missing
        LRatio = params.get("lowes_ratio", 0.70)  # 0.70 is default if key is missing
        dist_weight = params.get("distance_weight", 40)  # 40 is default if key is missing
        min_match_percnt = params.get("min_match_percnt", 30)  # 30 is default if key is missing
        max_match_percnt = params.get("max_match_percnt", 30)  # 30 is default if key is missing
        match_cnt_threshold = int((r1* min_match_percnt) / 100)
        max_matches = int((r1* max_match_percnt) / 100)

        output = {
                "debug": debug,
                "LRatio": int(LRatio*10000), 
                "max_matches": max_matches,
                "dist_weight": dist_weight, 
                "match_cnt_threshold": match_cnt_threshold,
                "in1": binary_des1,
                "in2": binary_des2
        }

        with open("circomInput.json", "w") as f:
                json.dump(output, f, indent=2)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
