"""lic_check.define."""

from pyquery.pyquery import PyQuery


class Segment(object):
    """License Segmentation.

    * Software Licenses
    * Documentation licenses
    * Other works
    """

    def __init__(self, element):
        """initialize."""
        self.name = element.get('id')
        self.description = element.text

    def __repr__(self):
        """representaion."""
        return self.name


class Category(object):
    """License Category.

    * GPL compatible licenses
    * GPL incompatible licenses
    * Nonfree Software licenses
    """

    def __init__(self, element):
        """initialize."""
        self.name = element.get('href').replace('#', '')
        self.description = element.text
        self.segment = None

    def __repr__(self):
        """representaion."""
        return self.name


class License(object):
    """License."""

    def __init__(self, element):
        """initialize."""
        self.name = element.get('id')
        self.description = element.text
        self.category = None
        self.segment = None

    def __repr__(self):
        """representaion."""
        return self.name


class Parse(object):
    """definition verious licences and comments about them."""

    def __init__(self, data):
        """initialize."""
        self.html = PyQuery(data)

    def segments(self):
        """segments.

        >>> with open('lic_check/license.html') as f:
        ...     data = f.read()
        >>> p = Parse(data)
        >>> p.segments()
        [SoftwareLicenses, DocumentationLicenses, OtherLicenses]
        """
        return [Segment(i) for i in self.html.find('.big-section h3')
                .filter(lambda i: i != 0)]

    def categories(self, segment):
        """categories.

        >>> with open('lic_check/license.html') as f:
        ...     data = f.read()
        >>> p = Parse(data)
        >>> len([i for i in p.categories(p.segments()[0])])
        3
        >>> p.categories(p.segments()[1])
        [FreeDocumentationLicenses, NonFreeDocumentationLicenses]
        >>> p.categories(p.segments()[2])
        [OtherLicenses, Fonts, OpinionLicenses, Designs]
        """
        return [Category(i)
                for i in self.html.find('.toc ul li a')
                .filter(lambda i, this: PyQuery(this)
                        .attr('href') == '#{0}'.format(segment))
                .siblings('ul').find('a')]

    def licenses(self, category):
        """licenses.

        >>> with open('lic_check/license.html') as f:
        ...     data = f.read()
        >>> p = Parse(data)
        >>> p.segments()[0]
        SoftwareLicenses
        >>> p.categories(p.segments()[0])[0]
        GPLCompatibleLicenses
        >>> len(p.licenses(p.categories(p.segments()[0])[0]))
        50
        >>> p.categories(p.segments()[0])[1]
        GPLIncompatibleLicenses
        >>> len(p.licenses(p.categories(p.segments()[0])[1]))
        40
        >>> len(p.licenses(p.categories(p.segments()[0])[2]))
        33
        """
        return [License(i)
                for i in (self.html
                          .find('.big-subsection h4#{0}'.format(category))
                          .parent().next_all('dl').eq(0).children('dt a'))
                if i.get('id') and i.text]
