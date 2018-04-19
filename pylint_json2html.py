"""Pylint JSON's report to HTML"""
import json
import collections

from jinja2 import Environment, PackageLoader, select_autoescape


ModuleInfo = collections.namedtuple('ModuleInfo', ['name', 'path'])


def build_jinja_env():
    env = Environment(
        loader=PackageLoader('pylint_json2html', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    return env


def build_reports_metrics(reports):
    """Build reports's metrics"""
    count_types = collections.Counter(
        line.get('type') or None
        for line in reports)
    count_modules = collections.Counter(
        line.get('module') or None
        for line in reports)
    count_symbols = collections.Counter(
        line.get('symbol') or None
        for line in reports)
    count_paths = collections.Counter(
        line.get('path') or None
        for line in reports)

    return {
        'types': count_types,
        'modules': count_modules,
        'symbols': count_symbols,
        'paths': count_paths,
    }


def build_reports_modules(reports):
    data = collections.defaultdict(list)
    for line in reports:
        module_name = line.get('module')
        module_path = line.get('path')
        module_info = ModuleInfo(
            module_name,
            module_path,
        )
        data[module_info].append(line)

    return data


def main():
    jinja_env = build_jinja_env()
    template = jinja_env.get_template('report.jinja2')
    filename = 'pylint.json'

    with open(filename) as fp:
        reports = json.load(fp)

    report = Report(reports)

    print(template.render(
        reports=reports,
        metrics=report.metrics,
        report=report,
    ))


class Report:
    """Pylint Report Representation

    We want to represent the pylint reports in various way, structuring the raw
    data (a list of messages) into something meaningful to work with and to
    display to an end-user.
    """
    def __init__(self, reports):
        self._reports = reports
        self._module_messages = build_reports_modules(reports)
        self._metrics = build_reports_metrics(reports)

    @property
    def modules(self):
        """Return a sequence of messages by modules ``(module, messages)``"""
        module_messages = (
            (module, sorted(messages, key=lambda x: x.get('line')))
            for module, messages in self._module_messages.items()
        )
        yield from sorted(module_messages, key=lambda x: x[0].path)

    @property
    def metrics(self):
        return self._metrics


if __name__ == '__main__':
    main()
