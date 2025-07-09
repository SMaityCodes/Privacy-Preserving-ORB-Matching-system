import cv2
import pickle
import argparse

def extract_orb_descriptors(image_path, n_features=100):
    """Extract ORB descriptors and keypoints from an image."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Error: Image not found at '{image_path}'")
    
    orb = cv2.ORB_create(nfeatures=n_features)
    keypoints, descriptors = orb.detectAndCompute(image, None)
    
    # Convert keypoints to serializable format
    kp_data = [{
        'pt': kp.pt,
        'size': kp.size,
        'angle': kp.angle,
        'response': kp.response,
        'octave': kp.octave,
        'class_id': kp.class_id
    } for kp in keypoints]
    
    return kp_data, descriptors

def save_to_pkl(data, output_file):
    """Save data to a .pkl file."""
    with open(output_file, 'wb') as f:
        pickle.dump(data, f)

def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Extract ORB descriptors from an image and save to a .pkl file.')
    parser.add_argument('-i', '--input', required=True, help='Input image filename')
    parser.add_argument('-o', '--output', required=True, help='Output .pkl filename')
    parser.add_argument('-n', '--num_features', type=int, default=100, help='Number of ORB features to extract (default: 100)')
    args = parser.parse_args()

    try:
        # Extract descriptors
        keypoints, descriptors = extract_orb_descriptors(args.input, args.num_features)
        
        # Save to pickle file
        save_to_pkl({'keypoints': keypoints, 'descriptors': descriptors}, args.output)
        
        # print(f"Successfully extracted {len(keypoints)} ORB descriptors and saved to '{args.output}'")
        # print(f"Descriptor shape: {descriptors.shape} (each descriptor is 32 bytes)")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
