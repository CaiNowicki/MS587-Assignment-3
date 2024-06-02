import fitz
import os

def extract_first_paragraph(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(2) # page numbering starts at 0, so page 2 is the 3rd page where the text starts
    text = page.get_text()

    #split the text into paragraphs
    paragraphs = text.split('\n\n')
    if paragraphs: #if the paragraphs exist
        first_paragraph = paragraphs[0].strip()
        return first_paragraph
    else:
        return None # return nothing if there are no paragraphs on that page

def process_from_folder(folder_path):
    #create folder to store txt files
    story_texts_folder = os.path.join(folder_path, 'story_texts')
    os.makedirs(story_texts_folder, exist_ok=True)
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'): # make sure we only grab PDF files
            pdf_path = os.path.join(folder_path, filename)
            first_paragraph = extract_first_paragraph(pdf_path)
            if first_paragraph:
                txt_filename = os.path.splitext(filename)[0] + '.txt'
                txt_path = os.path.join(story_texts_folder, txt_filename)
                with open(txt_path, 'w', encoding='utf-8') as txt_file: # open a new txt file for writing
                    txt_file.write(first_paragraph)
                print(f"Saved first paragraph from {filename} to {txt_filename}.")
            else:
                print(f"No text found on the third page of {filename}.")

folder_path = 'C:/Users/Admin/MS587 Web and SQL/MS587 - Assignment 1-2/MS587-Assignment-1-2/Animorphs/PDF'
process_from_folder(folder_path)