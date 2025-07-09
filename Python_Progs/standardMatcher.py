import cv2
import pickle
import numpy as np
import argparse

def load_pkl_data(pkl_file):
    """Load keypoints and descriptors from a .pkl file."""
    with open(pkl_file, 'rb') as f:
        data = pickle.load(f)
    if 'keypoints' not in data or 'descriptors' not in data:
        raise KeyError("Missing 'keypoints' or 'descriptors' in the .pkl file.")
    return data['keypoints'], data['descriptors']

def match_descriptors(desc1, desc2, ratio_thresh=0.7):
    """
    Match descriptors using Brute-Force + Lowe's ratio test.
    Returns: List of good matches.
    """
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(desc1, desc2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < ratio_thresh * n.distance:
            good_matches.append(m)

    return good_matches

def load_params(param_file):
    """
    Load parameters from a config file.
    Expected format: key=value (e.g., lowes_ratio=0.8)
    """
    params = {}
    with open(param_file, 'r') as f:
        for line in f:
            if '=' in line:
                key, val = line.strip().split('=', 1)
                params[key.strip()] = val.strip()
    return params

def main():
    parser = argparse.ArgumentParser(description='Count ORB matches between two .pkl files.')
    parser.add_argument('-pkl1', required=True, help='First .pkl file (e.g., desc1.pkl)')
    parser.add_argument('-pkl2', required=True, help='Second .pkl file (e.g., desc2.pkl)')
    parser.add_argument('-params', default='params.dat', help='Parameter file (default: params.dat)')
    args = parser.parse_args()

    try:
        # Load Lowe's ratio from parameter file
        params = load_params(args.params)
        lowes_ratio = float(params.get('lowes_ratio', 0.8))

        # Load descriptors
        kp1, desc1 = load_pkl_data(args.pkl1)
        kp2, desc2 = load_pkl_data(args.pkl2)

        desc1 = np.array(desc1, dtype=np.uint8)
        desc2 = np.array(desc2, dtype=np.uint8)

        if len(desc1) == 0 or len(desc2) == 0:
            raise ValueError("No descriptors found in one or both .pkl files.")

        # Perform descriptor matching
        good_matches = match_descriptors(desc1, desc2, lowes_ratio)

        # Output results
        print(f"Descriptors in {args.pkl1}: {len(desc1)}")
        print(f"Descriptors in {args.pkl2}: {len(desc2)}")
        print(f"Good matches (ratio={lowes_ratio}): {len(good_matches)}")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()

