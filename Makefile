
pylint.json: tests/*.py pylint_json2html/*.py
	pylint --load-plugins=pylint_json2html --output-format=jsonextended tests > pylint.json || exit 0

pylint.html: pylint.json pylint_json2html/templates/*.jinja2
	pylint-json2html --input-format jsonextended --output pylint.html pylint.json

pylint.simple.json: tests/*.py pylint_json2html/*.py
	pylint --output-format=json tests > pylint.simple.json || exit 0

pylint.simple.html: pylint.simple.json pylint_json2html/templates/*.jinja2
	pylint-json2html --input-format json --output pylint.simple.html pylint.simple.json
