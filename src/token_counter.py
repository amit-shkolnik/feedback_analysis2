import json
import os
from typing import List
import tiktoken  # Requires 'pip install tiktoken'
import config
from config import *

# Target size in tokens for each chunk (10,000 words ~ 13,000 - 15,000 tokens)
# We will use 15,000 tokens as the new, more precise limit.
TARGET_TOKEN_COUNT = config.token_chunk_size

def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    """
    Calculates the number of tokens in a string using the tiktoken library.
    
    Args:
        text: The string content to tokenize.
        model_name: The encoding to use. 'gpt-4' encoding is a good default 
                    for newer models and will give an accurate approximation.
                    
    Returns:
        The total number of tokens.
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # Fallback to a common encoding if the specific model name is not found
        encoding = tiktoken.get_encoding("cl100k_base") 
        
    return len(encoding.encode(text))

def split_json_to_token_chunks(file_path: str) -> List[str]:
    """
    Reads a large JSON file, converts it to a string, and splits it into chunks
    based on a target token count (15,000 tokens).

    Args:
        file_path: The path to the input JSON file.

    Returns:
        A list of strings, where each string is a chunk of the original JSON,
        limited by the TARGET_TOKEN_COUNT.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return []

    print(f"Reading file: {file_path}")

    # 1. Read the JSON file content as a single string
    try:
        # with open(file_path, 'r', encoding='utf-8') as f:
        #     raw_json_string = f.read()
        data_df=pd.read_csv(file_path)
        raw_json_string = data_df[:500].to_json(orient='records', force_ascii=False)

    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    # 2. Split the string into individual "words" (tokens/sections)
    # Using split() is a heuristic to create manageable chunks for the token counter.
    sections = raw_json_string.split() 

    total_tokens = count_tokens(raw_json_string)
    print(f"Total tokens in the JSON content (approximate): {total_tokens}")
    
    chunks: List[str] = []
    current_chunk_sections: List[str] = []
    
    # 3. Iterate through sections and build chunks
    for section in sections:
        # Check the token count of the current chunk + the new section
        test_chunk = " ".join(current_chunk_sections + [section])
        token_count = count_tokens(test_chunk)
        
        # If adding the next section pushes the chunk over the limit, finalize the current chunk
        if token_count > TARGET_TOKEN_COUNT and current_chunk_sections:
            chunks.append(" ".join(current_chunk_sections))
            current_chunk_sections = [section]  # Start a new chunk with the current section
            print(f"{len(chunks)} chunks created so far...")
        else:
            current_chunk_sections.append(section)

    # 4. Add the last remaining chunk
    if current_chunk_sections:
        chunks.append(" ".join(current_chunk_sections))

    print(f"Successfully split JSON into {len(chunks)} chunks.")
    return chunks

# --- Demonstration and Usage Example ---

def generate_mock_json_file(filename: str, num_records: int):
    """Generates a large mock JSON file for testing."""
    mock_data = []
    for i in range(1, num_records + 1):
        # Create a record with a lot of verbose, repeating text to simulate a large file size
        record = {
            "id": i,
            "title": f"Record {i} Title",
            "text_content": ("This is a verbose and repetitive text field designed " * 50) +
                            f"to significantly increase the word count of record {i}.",
            "metadata": {"source": "System_A", "timestamp": f"2024-01-01T10:{i:02d}:00Z"}
        }
        mock_data.append(record)
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Using a small indent for readability in the file
        json.dump(mock_data, f, indent=2)
    
    print(f"Generated mock JSON file: {filename} with {num_records} records.")


if __name__ == "__main__":
    # Define file name and number of records (adjust as needed to ensure file size > TARGET_TOKEN_COUNT)
    MOCK_FILENAME = "large_data.json"
    
    # Generate enough records to create multiple chunks
    RECORDS_TO_GENERATE = 150 # This will generate enough tokens to split into chunks.

    # 1. Generate the large mock file
    generate_mock_json_file(MOCK_FILENAME, RECORDS_TO_GENERATE)

    # 2. Run the splitter function
    json_chunks = split_json_to_token_chunks(MOCK_FILENAME)

    # 3. Verify the results
    print("\n--- Verification ---")
    
    for i, chunk in enumerate(json_chunks):
        token_count = count_tokens(chunk)
        print(f"Chunk {i+1}: {token_count} tokens (Limit: {TARGET_TOKEN_COUNT}).")
        
    # Example of using the token counter on a simple string:
    test_string = "Hello world! This is a test."
    test_tokens = count_tokens(test_string)
    print(f"\nTest string: '{test_string}' has {test_tokens} tokens.")
        
    # Clean up the mock file
    os.remove(MOCK_FILENAME)
    print(f"\nCleaned up mock file: {MOCK_FILENAME}")


text_to_check = "Your text goes here."
tokens = count_tokens(text_to_check)
print(f"Tokens: {tokens}")