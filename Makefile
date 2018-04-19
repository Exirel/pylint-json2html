
pylint.json: tests/*.py pylint_json2html.py
	pylint --load-plugins=pylint_json2html --output-format=jsonextended --reports=yes --score=yes tests > pylint.json || exit 0

pylint.html: pylint.json templates/*.jinja2
	pylint-json2html > pylint.html
