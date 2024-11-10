import sys
import base64
import zlib
import argparse
import requests

def compress_and_encode(file_path):
    """Reads, compresses, and base64-encodes the contents of the file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        compressed_content = zlib.compress(content.encode('utf-8'), 9)
        encoded_content = base64.urlsafe_b64encode(compressed_content).decode('ascii')
        
        return encoded_content

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def send_request(graph_type, encoded_content, output_file):
    """Sends a GET request to the Kroki API to render the encoded graph as an SVG, and saves it to a file."""
    url = f"https://kroki.io/{graph_type}/svg/{encoded_content}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        
        # Write the SVG content to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        print(f"SVG file saved as '{output_file}'")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while requesting the SVG: {e}")
        sys.exit(1)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Compress, base64-encode a .dot file, and request SVG from Kroki API.")
    parser.add_argument("file_path", help="Path to the .dot file")
    parser.add_argument("graph_type", help="Type of the graph (e.g., 'graphviz')")
    parser.add_argument("output_file", help="Output file name for the SVG")

    # Parse arguments
    args = parser.parse_args()
    
    # Process the file and get the encoded content
    encoded_content = compress_and_encode(args.file_path)
    
    # Send request to Kroki API and save SVG content to file
    send_request(args.graph_type, encoded_content, args.output_file)

if __name__ == "__main__":
    main()
