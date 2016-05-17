"""lic_check.define."""

from pyquery.pyquery import PyQuery


class License(object):
    """definition verious licences and comments about them."""

    def __init__(self, data):
        """initialize."""
        self.html = PyQuery(data)

    def segments(self):
        """segments.

        >>> with open('lic_check/license.html') as f:
        ...     data = f.read()
        >>> l = License(data)
        >>> l.segments()
        ['SoftwareLicenses', 'DocumentationLicenses', 'OtherLicenses']
        """
        return [i.get('id') for i in self.html.find('.big-section h3')
                .filter(lambda i: i != 0)]

    def categories(self, segment):
        """categories.

        >>> with open('lic_check/license.html') as f:
        ...     data = f.read()
        >>> l = License(data)
        >>> [i.replace('Licenses', '') for i in l.categories(l.segments()[0])]
        ['GPLCompatible', 'GPLIncompatible', 'NonFreeSoftware']
        >>> l.categories(l.segments()[1])
        ['FreeDocumentationLicenses', 'NonFreeDocumentationLicenses']
        >>> l.categories(l.segments()[2])
        ['OtherLicenses', 'Fonts', 'OpinionLicenses', 'Designs']
        """
        return [i.get('href').replace('#', '')
                for i in self.html.find('.toc ul li a')
                .filter(lambda i, this: PyQuery(this)
                        .attr('href') == '#{0}'.format(segment))
                .siblings('ul').find('a')]
