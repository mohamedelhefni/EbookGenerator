import os
import shutil
import zipfile
from markdown import markdown
from template.builder import *

def get_file_content(file):
    file_name = file.split('/')[-1].split('.')[0]
    content = ""
    content += f"#{file_name}\n"
    with open(file, 'r') as f:
        content += f.read()
    return {'title': file_name, 'content': markdown(content, output_format='xhtml')}


def generate_content(directory):
    if not os.path.isdir(directory):
        raise Exception("Please Enter Valid Directory")
    book = {}
    book['chapters'] = []
    book['content'] = []
    files = os.listdir(directory)
    for file in files:
        file_name = file.split('.')[0]
        file_path = directory + "/" + file
        book['chapters'].append(file_name)
        book['content'].append(get_file_content(file_path))
    return book


def generate_chapters(content):
    i = 1
    for book in content['content']:
        with open(f"tmp/OEBPS/chap{i}.xhtml", "w") as f:
            f.write(make_chapter(book))
        i += 1


def build_file(lang, file_content, file_toc, content, output):
    os.mkdir("tmp")
    os.mkdir("tmp/META-INF")
    os.mkdir("tmp/OEBPS")
    with open("./tmp/META-INF/container.xml", "w") as f:
        f.write(CONTAINER)
    with open("./tmp/OEBPS/stylesheet.css", "w") as f:
        f.write(make_stylesheet(lang))
    with open("./tmp/OEBPS/toc.ncx", "w") as f:
        f.write(file_toc)
    with open("./tmp/OEBPS/content.opf", "w") as f:
        f.write(file_content)
    generate_chapters(content)
    shutil.make_archive('output', 'zip', "tmp") 
    shutil.rmtree("tmp")
    with open("./mimetype", "w") as f:
        f.write(MIME_TYPE)
    z = zipfile.ZipFile('output.zip', 'a', zipfile.ZIP_DEFLATED) 
    z.write('mimetype')
    z.close()
    shutil.move("output.zip", f"{output}.epub")
    os.remove("mimetype")
    


def main():
    directory = input("Enter Directory path: ")
    title = input("Enter Book Title :")
    author = input("Enter Book author : ")
    lang = input("Enter book lang: ")
    output = input("Enter book output name: ")
    book_content = generate_content(directory)
    meta = make_content_meta(title, author, lang)
    file_content = content_file(meta, book_content['chapters']) 
    file_toc = book_toc(title, book_content['chapters'])
    build_file(lang, file_content, file_toc, book_content, output)


if __name__ == "__main__":
    main()
