#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Zope dependencies
#
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.fieldproperty import FieldProperty
from zope.component import getMultiAdapter

#
# Plone dependencies
#
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#
# z3c.forms dependencies
#
from z3c.form import group, field
from z3c.form.form import extends
from z3c.form.browser.textlines import TextLinesFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
#from plone.formwidget.contenttree import ObjPathSourceBinder

from collective.object.utils.source import ObjPathSourceBinder

#
# plone.app.widgets dependencies
#
from plone.app.widgets.dx import DatetimeFieldWidget, RelatedItemsFieldWidget

#
# DataGridFields dependencies
#
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from collective.z3cform.datagridfield.blockdatagridfield import BlockDataGridFieldFactory

# # # # # # # # # # # # # # # 
# Dexterity imports         # 
# # # # # # # # # # # # # # # 
from five import grok
from collective import dexteritytextindexer
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.content import Container
from plone.dexterity.browser import add, edit

# # # # # # # # # # # # # # # # # #
# !Exhibition specific imports!   #
# # # # # # # # # # # # # # # # # #
from collective.exhibition import MessageFactory as _
from .utils.vocabularies import *
from .utils.interfaces import *
from .utils.views import *

from collective.object.utils.widgets import AjaxSingleSelectFieldWidget, ExtendedRelatedItemsFieldWidget
from collective.z3cform.datagridfield.interfaces import IDataGridField
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from Acquisition import aq_inner
from zc.relation.interfaces import ICatalog

# # # # # # # # # # # # #
# # # # # # # # # # # # #
# Exhibition schema     #
# # # # # # # # # # # # #
# # # # # # # # # # # # #

from plone.app.content.interfaces import INameFromTitle
class INameFromPersonNames(INameFromTitle):
    def title():
        """Return a processed title"""

class NameFromPersonNames(object):
    implements(INameFromPersonNames)
    
    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.title

class IExhibition(form.Schema):
    
    text = RichText(
        title=_(u"Body"),
        required=False
    )

    priref = schema.TextLine(
        title=_(u'priref'),
        required=False
    )
    

    # # # # # # # # # # # # #
    # Exhibitions details   #
    # # # # # # # # # # # # #
    model.fieldset('exhibitions_details', label=_(u'Exhibitions details'), 
        fields=['title', 'exhibitionsDetails_exhibition_altTitle',
                'exhibitionsDetails_exhibitions_notes', 'exhibitionsDetails_organizingInstitution',
                'exhibitionsDetails_itinerary']
    )

    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )
    dexteritytextindexer.searchable('title')

    exhibitionsDetails_exhibition_altTitle = ListField(title=_(u'Alt. Title'),
        value_type=DictRow(title=_(u'Alt. Title'), schema=IAltTitle),
        required=False)
    form.widget(exhibitionsDetails_exhibition_altTitle=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('exhibitionsDetails_exhibition_altTitle')

    # Exhibition
   
    exhibitionsDetails_exhibitions_notes = ListField(title=_(u'Notes'),
        value_type=DictRow(title=_(u'Notes'), schema=INotes),
        required=False)
    form.widget(exhibitionsDetails_exhibitions_notes=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('exhibitionsDetails_exhibitions_notes')

    # Organizing institutions
    exhibitionsDetails_organizingInstitution = RelationList(
        title=_(u'Name'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type='PersonOrInstitution')
        ),
        required=False
    )
    form.widget('exhibitionsDetails_organizingInstitution', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')

    # Itinerary
    exhibitionsDetails_itinerary = ListField(title=_(u'Itinerary'),
        value_type=DictRow(title=_(u'Itinerary'), schema=IItinerary),
        required=False)
    form.widget(exhibitionsDetails_itinerary=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('exhibitionsDetails_itinerary')


    # # # # # # # # # #
    # Documentation   #
    # # # # # # # # # #
    model.fieldset('documentation', label=_(u'Documentation'), 
        fields=['documentation_documentation']
    )

    documentation_documentation = ListField(title=_(u'Documentation'),
        value_type=DictRow(title=_(u'Documentation'), schema=IDocumentationDocumentation),
        required=False)
    form.widget(documentation_documentation=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('documentation_documentation')


    # # # # # # # # # # #
    # Linked objects    #
    # # # # # # # # # # #

    model.fieldset('linked_objects', label=_(u'Linked Objects'), 
        fields=['linkedObjects_temp']
    )


    linkedObjects_temp = schema.TextLine(
        title=_(u'Object number'),
        required=False,
        default=u"",
        missing_value=u""
    )

    """linkedObjects_linkedobjects = RelationList(
        title=_(u'Object number'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(portal_type="Object")
        ),
        required=False
    )
    form.widget('linkedObjects_linkedobjects', ExtendedRelatedItemsFieldWidget, vocabulary='collective.object.relateditems')"""


# # # # # # # # # # # # # #
# Exhibition declaration  #
# # # # # # # # # # # # # #

class Exhibition(Container):
    grok.implements(IExhibition)
    pass

# # # # # # # # # # # # # #
# Exhibition add/edit views   # 
# # # # # # # # # # # # # #

class AddForm(add.DefaultAddForm):
    template = ViewPageTemplateFile('exhibition_templates/add.pt')
    def update(self):
        super(AddForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

        for widget in self.widgets.values():
            if widget.__name__ in ['IEventBasic.start', 'IEventBasic.end', 'IEventBasic.whole_day']:
                alsoProvides(widget, IFormWidget)

    def getRelatedObjects(self):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)

        source_object = self.context

        relations = catalog.findRelations(
            dict(to_id=intids.getId(aq_inner(source_object)),
                from_attribute="exhibitions_exhibition")
        )

        structure = ""
        for rel in list(relations):
            from_object = rel.from_object
            title = getattr(from_object, 'title', '')
            obj_number = getattr(from_object, 'identification_identification_objectNumber', '')
            url = from_object.absolute_url()
            structure += "<p><a href='%s'><span>%s</span> - <span>%s</span></a></p>" %(url, obj_number, title)

        return structure

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('exhibition_templates/edit.pt')

    def getRelatedObjects(self):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)

        source_object = self.context

        relations = catalog.findRelations(
            dict(to_id=intids.getId(aq_inner(source_object)),
                from_attribute="exhibitions_exhibition")
        )

        structure = ""
        for rel in list(relations):
            from_object = rel.from_object
            title = getattr(from_object, 'title', '')
            obj_number = getattr(from_object, 'identification_identification_objectNumber', '')
            url = from_object.absolute_url()
            structure += "<p><a href='%s'><span>%s</span> - <span>%s</span></a></p>" %(url, obj_number, title)

        return structure
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

        for widget in self.widgets.values():
            if widget.__name__ in ['IEventBasic.start', 'IEventBasic.end', 'IEventBasic.whole_day']:
                alsoProvides(widget, IFormWidget)





