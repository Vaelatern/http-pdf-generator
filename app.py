from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
import time
import yaml
from flask import Flask, request, render_template, render_template_string, Response

font_config = FontConfiguration()

app = Flask(__name__)

@app.route("/pdf/<filename>", methods=['GET', 'POST'])
def get_templated(filename):
    if request.method == 'GET':
        # Parse the YAML string
        data = yaml.safe_load(request.args.get('yaml', ''))
        template = lambda **x: render_template('baked-in.html', **x)
    elif request.method == 'POST':
        template_string = request.form.get('jinja2')
        if not template_string:
            return "Need 'jinja2' form element", 400
        # Parse the YAML string
        data = yaml.safe_load(request.form.get('yaml', ''))
        template = lambda **x: render_template_string(template_string, **x)

    rendered_template = template(**(data or {}))

    # Generate PDF using WeasyPrint
    html = HTML(string=rendered_template)
    pdf = html.write_pdf(font_config=font_config)

    # Prepare the PDF response
    response = Response(pdf, content_type='application/pdf')
    response.headers['Content-Disposition'] = f'inline; filename={filename}'
    return response

@app.route("/", methods=['GET', 'POST'])
def root():
    return 'TODO: put in some usage here'

if __name__ == '__main__':
    app.run()
