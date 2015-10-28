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

        basefilename = os.path.basename(filename)
        subprocess.check_call(["pdftohtml", "-noframes", basefilename], cwd=directory)

        htmlfilename = replace_extension(filename, "html")
        with open(htmlfilename, encoding="utf-8") as f:
            text = f.read()

        def process_and_replace(text, regex, process):
            r = re.compile(regex)

            paths = r.findall(text)
            to_replace = []

            for path in paths:
                to_replace.append((path, process(path)))

            return replace_links(text, to_replace)

        img_link_regex = 'src="({id}-[^"]*)"'.format(id=document_pk)

        def process_image(path):
            # Create a Image based on path.
            image = Image(document=doc)
            with open(directory + "/" + path, "rb") as f:
                image.img.save(path, File(f))
            return image.img.url

        internal_link_regex = 'href="({htmlfilename}#\d*)"'.format(htmlfilename=os.path.basename(htmlfilename))

        def process_link(path):
            return "#{}".format(path.split("#")[-1])

        text = process_and_replace(text, img_link_regex, process_image)
        text = process_and_replace(text, internal_link_regex, process_link)

        doc.html = strip_to_body_content(text)
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
