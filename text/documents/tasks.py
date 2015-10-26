import os
import re
import subprocess

from .models import Document, DocumentStatus, Image
from text.celery import app
from django.conf import settings
from django.core.files import File


@app.task()
def convert_to_html(document_pk):
    doc = Document.objects.get(pk=document_pk)
    doc.status = DocumentStatus.STARTED
    doc.save()
    try:
        doc.file.open('rb')

        directory = "{dirpath}/{id}/".format(dirpath=settings.PROCESSING_DIR, id=document_pk)
        if not os.path.exists(directory):
            # There can be a race condition here. But it's not a big deal.
            os.makedirs(directory)

        filename = "{directory}/{id}.pdf".format(directory=directory, id=document_pk)
        with open(filename, 'wb') as fw:
            fw.write(doc.file.file.read())
        doc.file.close()

        # TODO(att): if it fails, mark document appropriately
        basefilename = os.path.basename(filename)
        subprocess.check_call(["pdftohtml", "-noframes", basefilename], cwd=directory)

        htmlfilename = replace_extension(filename, "html")
        with open(htmlfilename) as f:
            text = f.read()

        r = re.compile('src="({id}-[^"]*)"'.format(id=document_pk))
        img_paths = r.findall(text)

        to_replace = []

        for img_path in img_paths:
            # Create a Image based on path.
            image = Image(document=doc)
            with open(directory + "/" + img_path, "rb") as f:
                image.img.save(img_path, File(f))
            # Change link in the original html.
            to_replace.append((img_path, image.img.url))
        new_text = replace_links(text, to_replace)
        doc.html = strip_to_body_content(new_text)
        doc.status = DocumentStatus.DONE
        doc.save()
    except:
        doc.status = DocumentStatus.ERROR
        doc.save()
        raise


def replace_links(text, to_replace):
    for old, new in to_replace:
        text = text.replace(old, new)
    return text


def replace_extension(filename, newextension):
    # Use only for simple use cases. Not bullet proof.
    extension = filename.split(".")[-1]
    newfilename = filename[:-len(extension)] + newextension
    return newfilename


def strip_to_body_content(html):
    # TODO(att): refactoring of regexes
    r = re.compile("<body [^>]*>")
    start_match = r.search(html)
    if start_match:
        html = html[start_match.end():]

    r = re.compile("<\\body[^>]*>")
    end_match = r.search(html)
    if end_match:
        html = html[:end_match.start()]
    return html
