# HTTP PDF Generator

This is a small service I use to help me rapidly churn out dozens or hundreds
of similar PDFs. I've used this to print personalized letters, with addresses
and names, sent by an organization.

## Core concepts

Templates are jinja2 formatted HTML. They can be strings or files (strings
reachable at a filename).

This tool takes HTML, passes it through a jinja2 template engine, and then
runs it through an HTML and CSS rendering engine to produce a streamed PDF.

## API surface

- `/` - GET, POST - TODO: will return usage
- `/pdf/<name.pdf>` - GET - When visited in a browser will load a PDF in your
  browser tab (or start a download) for that name. Accepts the variable `yaml`,
  which should be a yaml document that will be used in the jinja2 substitution.
- `/pdf/<name.pdf>` - POST - Requires the variable `jinja2` which is the
  template to turn into a PDF and return. Accepts the variable `yaml`,
  which should be a yaml document that will be used in the jinja2 substitution.

## Quickstart

```
podman build . --tag=http-pdf-generator:$(date -I)
podman run -p 5000:5000 http-pdf-generator:$(date -I) &
wget http://localhost:5000/pdf/read-me.pdf
wget -O read-me-with-templates.pdf http://localhost:5000/pdf/read-me-with-templates.pdf?yaml='{"name":"New User","render_type":"create","success":true,"magic":true}'
python3 ./testing.py this-is-a-post-example.pdf Woah madly
```

Then open `read-me.pdf` and `read-me-with-templates.pdf` which `wget`
just downloaded, and `this-is-a-post-example.pdf`

## Usage

Anything in the `assets` directory will be copied into the container,
reachable via your html template at `file:///assets/`. You can mount any
volume you like over `/assets` if you want to use that directory, or any
other, to be useful for your templates.

```
podman build . --tag=http-pdf-generator:$(date -I)
```

We use the container approach to get alpine with all the random fonts we
want. Customize this if you only want one font, you can get a MUCH more size
efficient image!

If you want to be able to edit the baked-in template (using the GET method) without a reload process:

```
podman run -p 5000:5000 -v $(pwd):/working/templates/:nocopy http-pdf-generator:$(date -I)
```

If you want to mount your current directory's assets over the existing assets

```
podman run -p 5000:5000 -v $(pwd)/assets:/assets http-pdf-generator:$(date -I)
```

## Considerations

### HTML

Weasyprint or the engines in use don't understand HTML tags with hyphens in
them, despite being perfectly fine in browsers. If you try to structure your
page with hyphens, you may run into some mess.

### CSS

We just use [https://weasyprint.org/](https://weasyprint.org/) as the engine
here. Feel free to put CSS inline in your HTML, or reference it some other way.

### Security

Be aware that the HTML engine can reach out to arbitrary endpoints unless you
have managed to disable that in your environment. Renders will take longer
than the longest duration you wait to load an asset. The default timeout at
time of writing is 10 seconds.  Do not expose this in your environment to
the general public without some serious soul-searching. If you can, use the
GET method and bake your HTML template into the image.

Weasyprint has a good page [on security
considations](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#security)

## License

OpenBSD-style ISC License

This tiny amount of code is a gift from me to others. And myself.

## Contributing

With consideration to Rich Hickey's [Design In Practice
(2023)](https://www.youtube.com/watch?v=c5QF2HjHLSE) and other people who
use this approach for ad-hoc and democratized project management, all commits
in this repository start with Problem: and have a second paragraph starting
with Solution:

This wastes some space.

This makes it clear we are all on the same page.

The vim project uses Problems and Solutions as the second lines of
commits. I've found it useful to have it as the first line of the commit too.

Match the commit format to have your contribution accepted.
