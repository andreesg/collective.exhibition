#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.exhibition import MessageFactory as _
from ..utils.vocabularies import _createPriorityVocabulary, _createInsuranceTypeVocabulary
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

priority_vocabulary = SimpleVocabulary(list(_createPriorityVocabulary()))
insurance_type_vocabulary = SimpleVocabulary(list(_createInsuranceTypeVocabulary()))

class ListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass

# # # # # # # # # # # # #
# Widget interface      #
# # # # # # # # # # # # #

class IFormWidget(Interface):
    pass


# # # # # # # # # # # # # #
# DataGrid interfaces     # 
# # # # # # # # # # # # # #

class IAltTitle(Interface):
    title = schema.TextLine(title=_(u'Title'), required=False)

class IOrganizingInstitutions(Interface):
    name = schema.TextLine(title=_(u'Name'), required=False)
    address = schema.TextLine(title=_(u'Address'), required=False)
    postalCode = schema.TextLine(title=_(u'Postal code'), required=False)
    place = schema.TextLine(title=_(u'label_place', default=u'Place'), required=False)
    country = schema.TextLine(title=_(u'Country'), required=False)
    telephone = schema.TextLine(title=_(u'Telephone'), required=False)
    fax = schema.TextLine(title=_(u'Fax'), required=False)

class IItinerary(Interface):
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    venue = schema.TextLine(title=_(u'Venue'), required=False)
    place = schema.TextLine(title=_(u'Place'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)
     
## Documentation
class IDocumentationDocumentation(Interface):
    article = schema.TextLine(title=_(u'Article'), required=False)
    title = schema.TextLine(title=_(u'Title'), required=False)
    author = schema.TextLine(title=_(u'Author'), required=False)
    pageMark = schema.TextLine(title=_(u'Page mark'), required=False)
    shelfMark = schema.TextLine(title=_(u'Shelf mark'), required=False)
    notes = schema.TextLine(title=_(u'Notes'), required=False)

## Linked Objects
class ILinkedObjects(Interface):
    objectNumber = schema.TextLine(title=_(u'Object number'), required=False)
    creator = schema.TextLine(title=_(u'Creator'), required=False)
    objectName = schema.TextLine(title=_(u'Object name'), required=False)
    title = schema.TextLine(title=_(u'Title'), required=False)

    

