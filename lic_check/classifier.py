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
        #: segment name
        self.name = element.get('id')
        #: description
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

    def __init__(self, element, segment):
        """initialize."""
        #: category name
        self.name = element.get('href').replace('#', '')
        #: description
        self.description = element.text
        #: belonged segment
        self.segment = segment

    def __repr__(self):
        """representaion."""
        return self.name


class License(object):
    """License."""

    def __init__(self, element, category):
        """initialize."""
        #: license name
        self.name = element.get('id')
        #: description
        self.description = element.text
        #: belonged category
        self.category = category
        #: belonged segment
        self.segment = self.category.segment

    def __repr__(self):
        """representaion."""
        return self.name


class Classifier(object):
    """classify verious licences.

    >>> c = Classifier()
    >>> c.segments
    [SoftwareLicenses, DocumentationLicenses, OtherLicenses]
    >>> c.segments[0].categories
    [GPLCompatibleLicenses, GPLIncompatibleLicenses, NonFreeSoftwareLicenses]
    >>> c.segments[0].categories[0].licenses
    [GNUGPLv3, GPLv2, LGPLv3, LGPLv2.1, AGPLv3.0, ...
    """

    default_data = 'lic_check/license.html'

    def __init__(self):
        """initialize."""
        with open(self.default_data) as fobj:
            data = fobj.read()
        self.html = PyQuery(data)
        self.segments = self._parse()

    def _parse(self):
        """parse license html."""
        segments = []
        for segment in self._segments():
            segment.categories = self.categories(segment)
            for category in segment.categories:
                category.licenses = self.licenses(category)
            segments.append(segment)
        return segments

    def _segments(self):
        """segments."""
        return (Segment(i) for i in self.html.find('.big-section h3')
                .filter(lambda i: i != 0))

    def categories(self, segment=None):
        """categories.

        >>> c = Classifier()
        >>> c.categories(c.segments[0])
        [GPLCompatibleLicenses, GPLIncompatibleLicenses, NonFreeSoftware...
        >>> c.categories(c.segments[1])
        [FreeDocumentationLicenses, NonFreeDocumentationLicenses]
        >>> c.categories(c.segments[2])
        [OtherLicenses, Fonts, OpinionLicenses, Designs]
        >>> c.categories().get('SoftwareLicenses')
        [GPLCompatibleLicenses, GPLIncompatibleLicenses, NonFreeSoftware...
        >>> c.categories().get('DocumentationLicenses')
        [FreeDocumentationLicenses, NonFreeDocumentationLicenses]
        """
        if segment:
            return [Category(i, segment)
                    for i in self.__retrieve_cat_elem(segment)]
        else:
            return {'{0}'.format(_seg): self.categories(_seg)
                    for _seg in self.segments}

    def __retrieve_cat_elem(self, segment):
        return (self.html.find('.toc ul li a')
                .filter(lambda i, this: PyQuery(this)
                        .attr('href') == '#{0}'.format(segment))
                .siblings('ul').find('a'))

    def licenses(self, category=None):
        """licenses.

        >>> c = Classifier()
        >>> sw_lic = c.segments[0]
        >>> gpl_compat_lic = c.categories(sw_lic)[0]
        >>> gpl_compat_lics = c.licenses(gpl_compat_lic)
        >>> len(gpl_compat_lics)
        50
        >>> gpl_compat_lics[0]
        GNUGPLv3
        >>> gpl_compat_lics[0].category
        GPLCompatibleLicenses
        >>> gpl_compat_lics[0].segment
        SoftwareLicenses
        >>> gpl_incompat_lic = c.categories(c.segments[0])[1]
        >>> c.licenses(gpl_incompat_lic)
        [AGPLv1.0, AcademicFreeLicense, apache1.1, ...
        >>> nonfree_lic = c.categories(sw_lic)[2]
        >>> c.licenses(nonfree_lic)
        [NoLicense, Aladdin, apsl1, ...
        >>> c.licenses().get('GPLCompatibleLicenses')
        [GNUGPLv3, GPLv2, LGPLv3, LGPLv2.1, AGPLv3.0, ...
        """
        if category:
            return [License(i, category)
                    for i in self.__retrieve_lic_elem(category)
                    if i.get('id') and i.text]
        else:
            categories = []
            for i in self.categories().values():
                categories += i
            return {'{0}'.format(cat): self.licenses(cat)
                    for cat in categories}

    def __retrieve_lic_elem(self, category):
        return (self.html.find('.big-subsection h4#{0}'.format(category))
                .parent().next_all('dl').eq(0).children('dt a'))
