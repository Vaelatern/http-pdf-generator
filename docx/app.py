import time
import yaml
import tempfile
import os.path
from subprocess import Popen

from flask import Flask, request, render_template, render_template_string, Response
from docxtpl import DocxTemplate
from docx2pdf import convert

app = Flask(__name__)

def docx_to_pdf(filename):
    p = Popen(["libreoffice", "--headless", "--convert-to", "pdf",
                   "--outdir", os.path.dirname(filename),
                   filename],
              env={"HOME": "/tmp"})
    p.communicate()

def prepare_docx_file():
    doc = DocxTemplate(filename)
    doc.render(data)

@app.route("/pdf/<filename>", methods=['GET'])
def get_templated(filename):
    # Parse the YAML string
    data = yaml.safe_load(request.args.get('yaml', '')) or {}

    doc = DocxTemplate('baked-in.docx')
    doc.render(data)
    tmpfile = tempfile.NamedTemporaryFile()
    doc.save(tmpfile.name)

    # Generate PDF using libreoffice
    docx_to_pdf(tmpfile.name)

    # Prepare the PDF response
    with open(tmpfile.name+'.pdf', 'rb') as fp:
        response = Response(fp.read(), content_type='application/pdf')
    response.headers['Content-Disposition'] = f'inline; filename={filename}'
    return response

@app.route("/", methods=['GET', 'POST'])
def root():
    return 'TODO: put in some usage here'

if __name__ == '__main__':
    app.run()
