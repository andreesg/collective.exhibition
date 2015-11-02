#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from collective.exhibition import MessageFactory as _
from ..utils.vocabularies import _createPriorityVocabulary, _createInsuranceTypeVocabulary
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.directives import dexterity, form

from collective.object.utils.source import ObjPathSourceBinder
from collective.object.utils.variables import *
from collective.object.utils.widgets import AjaxSingleSelectFieldWidget

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from collective.object.utils.widgets import SimpleRelatedItemsFieldWidget
from plone.directives import dexterity, form

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


class INotes(Interface):
    note = schema.Text(title=_(u'Notes'), required=False)

class IAltTitle(Interface):
    title = schema.TextLine(title=_(u'Alt. Title'), required=False)
    type = schema.TextLine(title=_(u'Type'), required=False)

class IOrganizingInstitutions(Interface):
    name = RelationList(
        title=_(u'Name'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('name', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')


class IItinerary(Interface):
    startDate = schema.TextLine(title=_(u'Start date'), required=False)
    endDate = schema.TextLine(title=_(u'End date'), required=False)
    venue = RelationList(
        title=_(u'Venue'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type="PersonOrInstitution")
        ),
        required=False
    )
    form.widget('venue', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    form.widget('place', AjaxSingleSelectFieldWidget,  vocabulary="collective.exhibition.places")
    place = schema.List(
        title=_(u'label_place', default=u'Place'),
        required=False,
        value_type=schema.TextLine(),
        missing_value=[]
    )

    notes = schema.Text(title=_(u'Notes'), required=False)
     
## Documentation
class IDocumentationDocumentation(Interface):
    article = schema.TextLine(title=_(u'Article'), required=False)
    title = RelationList(
        title=_(u'Title'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder()
        ),
        required=False
    )
    form.widget('title', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    pageMark = schema.TextLine(title=_(u'Page mark'), required=False)
    notes = schema.Text(title=_(u'Notes'), required=False)

## Linked Objects
class ILinkedObjects(Interface):
    objectNumber = RelationList(
        title=_(u'Object number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type="Object")
        ),
        required=False
    )
    form.widget('objectNumber', SimpleRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    

