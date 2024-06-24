# import pyodbc
# import os
# import re

# # Function to establish database connection
# def connect_to_database():
#     driver = '{ODBC Driver 17 for SQL Server}'
#     server = 'DESKTOP-P2UO69O\SQLEXPRESS'
#     database = 'AnimorphsSite'
#     conn_str = (
#         f'DRIVER={driver};'
#         f'SERVER={server};'
#         f'DATABASE={database};'
#         'Trusted_Connection=yes;'
#         'Encrypt=yes;'
#         'TrustServerCertificate=yes'
#     )
#     try:
#         conn = pyodbc.connect(conn_str)
#         return conn
#     except pyodbc.Error as e:
#         print(f"Error connecting to SQL Server: {e}")
#         return None

# # Main function to execute the script
# def main():

#     cover_dir = r'C:\Users\Admin\MS587 Web and SQL\MS587-Assignment-3\MS587-Assignment-3\Animorphs\cover_images'
#     cover_pattern = re.compile(r'Ani (\d+) - (.+) - (.+)_cover\.png', re.IGNORECASE)
    
#     # Connect to the database
#     conn = connect_to_database()
#     if conn:
#         try:
#             cursor = conn.cursor()

#             # Process cover images
#             for filename in os.listdir(cover_dir):
#                 match = cover_pattern.match(filename)
#                 if match:
#                     vol_num, book_title, author_name = match.groups()
#                     first_name, last_name = author_name.split(' ', 1)
#                     cover_path = os.path.join(cover_dir, filename)
                    
#                     # Insert into Authors (if not already exists)
#                     cursor.execute("""
#                         IF NOT EXISTS (SELECT 1 FROM Authors WHERE col_last_name = ? AND col_first_name = ?)
#                         INSERT INTO Authors (col_first_name, col_last_name, col_isHuman)
#                         OUTPUT inserted.pk_auth_ID
#                         VALUES (?, ?, 1);
#                         """, last_name, first_name, first_name, last_name)

#                     author_id = cursor.fetchone()[0]

#                     # Insert into Books with cover image path
#                     cursor.execute("""
#                         INSERT INTO Books (col_book_title, col_book_cover_path, fk_auth_ID)
#                         VALUES (?, ?, ?);
#                         """, book_title, cover_path, author_id)

#                     print(f'Processed cover: {filename}')

#             # Commit changes
#             conn.commit()
#             print("Changes committed successfully.")

#         except pyodbc.Error as e:
#             print(f"Error executing SQL query: {e}")

#         finally:
#             # Close database connection
#             conn.close()
#             print("Database connection closed.")

#     else:
#         print("Failed to connect to the database.")

# # Execute the main function
# if __name__ == "__main__":
#     main()

import os
import csv
import re

# File paths
base_dir = r'C:\Users\Admin\MS587 Web and SQL\MS587-Assignment-3\MS587-Assignment-3'
cover_dir = os.path.join(base_dir, 'Animorphs', 'cover_images')
story_texts_dir = os.path.join(base_dir, 'Animorphs', 'story_texts')
cover_metadata_file = os.path.join(base_dir, 'cover_metadata.csv')

# Define patterns for matching filenames
cover_pattern = re.compile(r'Ani (\d+(\.\d+)?) - (.+) - (.+)_cover\.png')
story_text_pattern = re.compile(r'Ani_(\d+(\.\d+)?)___(.+?)___(.+)\.txt')
audiobook_pattern = re.compile(r'Ani_(\d+(\.\d+)?)___(.+?)___(.+)\.mp3')

# Utility function to read file contents
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f'Error reading {file_path}: {e}')
        return None

# Collect metadata
metadata = []

# Logging to identify issues
unmatched_files = []

# Iterate through story text files
for filename in os.listdir(story_texts_dir):
    if filename.endswith('.txt'):
        match = story_text_pattern.match(filename)
        if match:
            vol_num, book_title, author_name = match.groups()[:3]
            text_file_path = os.path.join(story_texts_dir, filename)
            text_contents = read_text_file(text_file_path)

            # Find corresponding audiobook file
            audiobook_file_path = text_file_path.replace('.txt', '.mp3')
            if not os.path.exists(audiobook_file_path):
                audiobook_file_path = None

            # Find corresponding cover image
            cover_filename = f"Ani {vol_num} - {book_title.replace('_', ' ')} - {author_name.replace('_', ' ')}_cover.png"
            cover_file_path = os.path.join(cover_dir, cover_filename)
            if not os.path.exists(cover_file_path):
                cover_file_path = None

            metadata.append([vol_num, book_title.replace('_', ' '), author_name.replace('_', ' '), text_contents, cover_file_path, audiobook_file_path])
        else:
            unmatched_files.append(filename)

# Report unmatched files
if unmatched_files:
    print(f"Unmatched files: {unmatched_files}")

# Write metadata to CSV
with open(cover_metadata_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['vol_num', 'book_title', 'author_name', 'book_contents', 'cover_file_path', 'audiobook_path'])
    writer.writerows(metadata)

print('Metadata extraction complete.')

