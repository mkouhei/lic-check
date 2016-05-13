"""lic_check."""

# based on https://www.gnu.org/licenses/license-list.en.html


SEGMENTS = {'SoftwareLicenses': 'Software Licenses',
            'DocumentationLicenses': 'Licenses For Documentation',
            'OtherWorksLicenses': 'Licenses for Other Works'}

SOFTWARE_LICENSES = {
    'GPLCompatibleLicenses': 'GPL-Compatible Free Software Licenses',
    'GPLIncompatibleLicenses': 'GPL-Incompatible Free Software Licenses',
    'NonFreeSoftwareLicenses': 'Nonfree Software Licenses'}

DOCUMENTATION_LICENSES = {
    'FreeDocumentationLicenses': 'Free Documentation Licenses',
    'NonFreeDocumentationLicenses': 'Nonfree Documentation Licenses'}

OTHER_WORKS_LICENSES = {
    'OtherLicenses': ('Licenses for Works of Practical Use '
                      'besides Software and Documentation'),
    'Fonts': 'Licenses for Fonts',
    'OpinionLicenses': ('Licenses for Works stating a Viewpoint'
                        '(e.g., Opinion or Testimony)'),
    'Designs': 'Licenses for Designs for Physical Objects'}
