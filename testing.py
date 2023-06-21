import urllib.parse
import http.client
import sys

PORT = 5000
ADDR = 'localhost'

JINJA_TEMPLATE = '''
<style>
body { display: flex; justify: space-around; flex-direction: column; }
body>* { margin-top: 30%; }
</style>
<body>
<div>
Here is an example MadLibs.
</div>
{% if give_example %}
<div>
"{{ exclamation }}! he said {{ adverb }} as he jumped into his convertible {{ noun }} and drove off with his {{ adjective }} wife."
</div>
{% else %}
<div>
Syke! No mad libs today.
</div>
{% endif %}
</body>
'''

def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <filename> [<exclamation> <adverb> <noun> <adjective>]')
        sys.exit(1)

    filename = sys.argv[1]
    _give_example = len(sys.argv) > 2
    _exclamation = sys.argv[2] if len(sys.argv) > 2 else ''
    _adverb = sys.argv[3] if len(sys.argv) > 3 else ''
    _noun = sys.argv[4] if len(sys.argv) > 4 else ''
    _adjective = sys.argv[5] if len(sys.argv) > 5 else ''

    import json
    yaml_data = json.dumps({"give_example": _give_example,
                            "exclamation": _exclamation,
                            "adverb": _adverb,
                            "noun": _noun,
                            "adjective": _adjective
                            })

    def urlencode(string):
        # Use urllib.parse.quote() to perform URL encoding
        return urllib.parse.quote(string)

    jinja2_encoded = urlencode(JINJA_TEMPLATE)

    url = f'{ADDR}:{PORT}'
    params = f'jinja2={jinja2_encoded}&yaml={urlencode(yaml_data)}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    conn = http.client.HTTPConnection(url)
    conn.request('POST', f'/pdf/{filename}', params, headers)
    response = conn.getresponse()

    with open(filename, 'wb') as file:
        file.write(response.read())
    conn.close()

if __name__ == '__main__':
    main()
