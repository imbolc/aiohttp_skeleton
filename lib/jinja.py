from jinja2 import BaseLoader, TemplateNotFound
from os.path import join, getmtime


class AppsLoader(BaseLoader):

    def __init__(self, templates_path='templates', apps_path='apps'):
        self.templates_path = templates_path
        self.apps_path = apps_path

    def get_source(self, environment, template):
        for filename in self.get_filenames(template):
            try:
                with open(filename, 'rt', encoding='utf-8') as f:
                    source = f.read()
                break
            except IOError:
                pass
        else:
            raise TemplateNotFound(template)
        mtime = getmtime(filename)
        return source, filename, lambda: mtime == getmtime(filename)

    def get_filenames(self, template):
        """
            >>> loader = AppsLoader()

            >>> loader.get_filenames('index.html')
            ['templates/index.html']

            >>> loader.get_filenames('foo/bar/baz.html')
            ['templates/foo/bar/baz.html', 'apps/foo/templates/bar/baz.html']
        """
        filenames = [join(self.templates_path, template)]
        if '/' in template:
            app, tpl = template.split('/', 1)
            filename = join(self.apps_path, app, self.templates_path, tpl)
            filenames.append(filename)
        return filenames


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
