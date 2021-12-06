import uuid
import datetime

MIME_TYPE = "application/epub+zip"

book_uuid = uuid.uuid4()

def make_stylesheet(lang):
    text = ""
    text += """
    p {text-indent: .3in;
        margin-left:0;
        margin-right:0;
        margin-top:0;
        margin-bottom:0;
        text-align: justify
        }

    html, body {

        margin-left:2%;
        margin-right:2%;
        margin-top:2%;
        margin-bottom:2%;
    """
    text += "direction: rtl;" if lang == 'ar' else "direction: ltr;"
    text += "}"

    return text


CONTAINER = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def make_content_meta(title, author, lang):
    return f"""
        <dc:identifier id="uuid_id" opf:scheme="uuid">{book_uuid}</dc:identifier>
        <dc:identifier opf:scheme="calibre">{book_uuid}</dc:identifier>
        <dc:language>{lang}</dc:language>
        <dc:title>{title}</dc:title>
        <dc:creator opf:file-as="{author}" opf:role="aut">{author}</dc:creator>
        <meta name="calibre:title_sort" content="{title}"/>
        <dc:date>{datetime.datetime.now().isoformat()}</dc:date>
        """


def make_content_manifest(chapters):
    text = ""
    for i in range(1,len(chapters) + 1):
        text += f'<item id="chapter{i}" href="chap{i}.xhtml" media-type="application/xhtml+xml" />\n'
    return text


def make_content_spine(chapters):
    text = ""
    for i in range(1, len(chapters) + 1):
        text += f'<itemref idref="chapter{i}" /> \n' 
    return text




def content_file(meta,chapters):
    return f"""<?xml version='1.0' encoding='utf-8'?>
    <package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
     <metadata xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:opf="http://www.idpf.org/2007/opf">
       {meta}
     </metadata>
     <manifest>
      <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
      <item id="style" href="stylesheet.css" media-type="text/css" />
      {make_content_manifest(chapters)}
     </manifest>
     <spine toc="ncx">
      {make_content_spine(chapters)}
     </spine>
    </package>
    """



# make table of content from chapters
def make_navmap(chapters):
    text = ""
    for i in range(1, len(chapters) + 1):
        text += f"""
            <navPoint id="chapter{i}" playOrder="{i - 1}">
              <navLabel>
                <text>{chapters[i - 1]}</text>
              </navLabel>
              <content src="chap{i}.xhtml"/>
            </navPoint>
        """
    return text




# make book table of content
def book_toc(title, chapters):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
          <head>
            <meta name="dtb:uid" content="{book_uuid}"/>
            <meta name="dtb:depth" content="1"/>
            <meta name="dtb:totalPageCount" content="0"/>
            <meta name="dtb:maxPageNumber" content="0"/>
          </head>
          <docTitle>
            <text>{title}</text>
          </docTitle>
          <navMap>
          {make_navmap(chapters)}
         </navMap>
        </ncx>
        """

# make each chapter 
def make_chapter(chapter):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>{chapter['title']}</title>
<link href="stylesheet.css" type="text/css" rel="stylesheet" />
</head>
<body>
{chapter['content']}
</body>
</html>
    """


