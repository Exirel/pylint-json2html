# pylint-json2html

A pylint JSON report file to HTML: pylint is used to generate a JSON report,
and this tool will transform this report into an HTML document:

    usage: pylint-json2html [-h] [-o FILENAME] [-e OUTPUT_ENCODING]
                            [-t FILENAME] [-f FORMAT] [FILENAME]

    Transform Pylint JSON report to HTML

    positional arguments:
    FILENAME              Pylint JSON report input file (or stdin)

    optional arguments:
    -h, --help          show this help message and exit
    -o FILENAME, --output FILENAME
                        Pylint HTML report output file (or stdout)
    -e ENCODING, --encoding ENCODING
                        Encoding used to write output file (if not stdout);
                        default to utf-8
    -t FILENAME, --template FILENAME
                        Jinja2 custom template to generate report
    -f FORMAT, --input-format FORMAT
                        Pylint JSON Report input type (json or jsonextended)

## Why?

Since its [1.7 version](https://pylint.readthedocs.io/en/latest/whatsnew/1.7.html#removed-changes),
Pylint does not provide an HTML output format. The release notes say that:

> It was lately a second class citizen in Pylint, being mostly neglected.
> Since we now have the JSON reporter, it can be used as a basis for building
> more prettier HTML reports than what Pylint can currently generate.
> This is part of the effort of removing cruft from Pylint, by removing less
> used features.

And I agree with that statements. Few people use the HTML reports, and pylint
is getting old. Its core features are complex and they require a lot of times
and efforts - and I am thankful for that software to exist in the first place!

So here it is: a plugin to fulfill my own needs. I share it as open-source
because why not?

## Installation

To install this tool, use pip:

    (venv) $ pip install pylint-json2html

You can always download the sources from the github repository, and use the
`setup.py` file to `install` or `develop`, but I would not recommend that
unless you plan to contribute to this small project of mine.

## Usage

My favorite way of using `pylint` and `pylint-json2html` is this one:

    (venv) $ pylint my_package | pylint-json2html -o pylint.html

Provided that you configure your Pylint config file with:

    [REPORTS]
    output-format=json

But you can generate first a JSON file, then use `pylint-json2html` to read it:

    (venv) $ pylint your_package > pylint.json
    (venv) $ pylint-json2html -o pylint.html pylint.json

You can also redirect `pylint-json2html`'s stdout:

    (venv) $ pylint-json2html pylint.json > pylint.html

You can specify the output encoding used to write to your file. Note that you
can't do that with stdout (you will have to configure your environment's locale
if you want to control that):

    (venv) $ pylint-json2html -o pylint.html -e utf-8 pylint.json

This is especially usefull when your locale is something like `cp1252` or
`latin1`, and you want to make sure your output file is properly written as
utf-8 (as it should be when working with Python file).

## Extended Report

Actually, I lied about my favorite way, it is this one:

    (venv) $ pylint my_package | pylint-json2html -f jsonextended -o pylint.html

With this Pylint configuration:

    [MASTER]
    load-plugins=pylint_json2html

    [REPORTS]
    output-format=jsonextended

The `pylint_json2html` is a Pylint plugin that adds a new output format:
`jsonextended`. By default, the `json` format contains only a list of messages,
and this new format contains also metrics, such the number of analysed
statements, or the list of dependencies.

The configuration above can be tested using the command line instead:

    (venv) $ pylint --load-plugins=pylint_json2html \
                    --output-format=jsonextended your_package > pylint.json

Then, you will be able to use the JSON extended report to generate an HTML
report:

    (venv) $ pylint-json2html -f jsonextended -o pylint.html pylint.json

And voilà!

## Custom Template

This plugin uses a Jinja2 template to generate the HTML output, but you may
need your own template. For that purpose, you can use the option
`-t/--template`, like this:

    (venv) $ pylint-json2html -f jsonextended -t custom.tpl -o pylint.html pylint.json

### Report

In your template you have access to a `report` object:

* `report.score`: score given by pylint, available only with
  `jsonextended` format
* `report.previous_score`: previous score given by pylint, available only with
  `jsonextended` format
* `report.modules`: a list of 2-value tuple: `(module, messages)`

The `module` object:

* `module.name`: name of the module
* `module.path`: path to the module's file

The `messages` value is a list of dict, each with the following keys:

* `line`
* `column`
* `type`
* `symbol`
* `message-id`
* `obj`
* `message`

### Metrics

In your template you have access to a `metrics` dict with the following keys:
`types`, `symbols`, `modules`, `paths`. Each of them contains a dict.

### Encoding

The default template contains that header:

    <meta charset="utf-8">

So if you want to use a different output encoding, make sure that:

1. you can actually encode the characters from pylint's output with that
   encoding
2. and also that you use your own custom template to change that meta tag,
   otherwise that might not look very good in a browser
