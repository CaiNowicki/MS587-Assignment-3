import os

books_directory = os.path.abspath(r'C:\Users\Admin\MS587 Web and SQL\MS587 - Assignment 1-2\MS587-Assignment-1-2\Animorphs\PDF')

os.makedirs(books_directory, exist_ok=True)
# Get the list of all PDF files in the directory
pdf_files = [f for f in os.listdir(books_directory) if f.endswith('.pdf')]

# Get the base directory (the directory containing the script)
base_directory = os.path.dirname(os.path.abspath(__file__))

# Debug: print the found PDF files
print(f"PDF files found: {pdf_files}")

# Create or overwrite the books.txt file
with open('books.txt', 'w') as file:
    for pdf in pdf_files:
        title = os.path.splitext(pdf)[0]  # Get the title from the filename without extension
        abs_path = os.path.join(books_directory, pdf)
        rel_path_index = abs_path.find('Animorphs')  # Find the index of 'Animorphs' in the absolute path
        if rel_path_index != -1:
            rel_path = abs_path[rel_path_index:]  # Get the relative path starting from 'Animorphs'
            file.write(f"{title},{rel_path}\n")

print("books.txt file created successfully.")

def remove_animorphs_pdf(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()
    
    # Remove every occurrence of 'Animorphs\PDF'
    modified_content = content.replace('Animorphs\\PDF', '')
    modified_content = modified_content.replace('\\', '')

    with open(output_file, 'w') as file:
        file.write(modified_content)

# Example usage:
input_file = 'books.txt'
output_file = 'books_modified.txt'
remove_animorphs_pdf(input_file, output_file)
print(f"Occurrences of 'Animorphs\\PDF' removed from '{input_file}'. Modified content saved to '{output_file}'.")
