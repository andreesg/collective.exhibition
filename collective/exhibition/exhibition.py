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

#
# plone.app.widgets dependencies
#
from plone.app.widgets.dx import DatetimeFieldWidget

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

# # # # # # # # # # # # #
# # # # # # # # # # # # #
# Exhibition schema     #
# # # # # # # # # # # # #
# # # # # # # # # # # # #

class IExhibition(form.Schema):

    start_date = schema.Datetime(
        title=_(u'label_event_start', default=u'Event Starts'),
        required=False
    )
    dexteritytextindexer.searchable('start_date')
    form.widget(start_date=DatetimeFieldWidget)

    end_date = schema.Datetime(
        title=_(u'label_event_end' ,default=u'Event Ends'),
        required=False
    )
    dexteritytextindexer.searchable('end_date')
    form.widget(end_date=DatetimeFieldWidget)
    
    text = RichText(
        title=_(u"Body"),
        required=False
    )

    # # # # # # # # # # # # #
    # Exhibitions details   #
    # # # # # # # # # # # # #
    model.fieldset('exhibitions_details', label=_(u'Exhibitions details'), 
        fields=['exhibitionsDetails_exhibition_title', 'exhibitionsDetails_exhibition_altTitle',
                'exhibitionsDetails_exhibition_startDate', 'exhibitionsDetails_exhibition_endDate',
                'exhibitionsDetails_exhibition_notes', 'exhibitionsDetails_organizingInstitutions',
                'exhibitionsDetails_itinerary']
    )

    # Exhibition
    exhibitionsDetails_exhibition_title = schema.TextLine(
        title=_(u'Title'),
        required=False
    )
    dexteritytextindexer.searchable('exhibitionsDetails_exhibition_title')

    exhibitionsDetails_exhibition_altTitle = ListField(title=_(u'Alt. Title'),
        value_type=DictRow(title=_(u'Alt. Title'), schema=IAltTitle),
        required=False)
    form.widget(exhibitionsDetails_exhibition_altTitle=DataGridFieldFactory)
    dexteritytextindexer.searchable('exhibitionsDetails_exhibition_altTitle')

    exhibitionsDetails_exhibition_startDate = schema.TextLine(
        title=_(u'Start date'),
        required=False
    )
    dexteritytextindexer.searchable('exhibitionsDetails_exhibition_startDate')

    exhibitionsDetails_exhibition_endDate = schema.TextLine(
        title=_(u'End date'),
        required=False
    )
    dexteritytextindexer.searchable('exhibitionsDetails_exhibition_endDate')

    exhibitionsDetails_exhibition_notes = schema.TextLine(
        title=_(u'Notes'),
        required=False
    )
    dexteritytextindexer.searchable('exhibitionsDetails_exhibition_notes')

    # Organizing institutions
    exhibitionsDetails_organizingInstitutions = ListField(title=_(u'Organizing institutions'),
        value_type=DictRow(title=_(u'Organizing institutions'), schema=IOrganizingInstitutions),
        required=False)
    form.widget(exhibitionsDetails_organizingInstitutions=BlockDataGridFieldFactory)
    dexteritytextindexer.searchable('exhibitionsDetails_organizingInstitutions')

    # Itinerary
    exhibitionsDetails_itinerary = ListField(title=_(u'Itinerary'),
        value_type=DictRow(title=_(u'Itinerary'), schema=IItinerary),
        required=False)
    form.widget(exhibitionsDetails_itinerary=DataGridFieldFactory)
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
        fields=['linkedObjects_linkedObjects']
    )

    linkedObjects_linkedObjects = ListField(title=_(u'Linked Objects'),
        value_type=DictRow(title=_(u'Linked Objects'), schema=ILinkedObjects),
        required=False)
    form.widget(linkedObjects_linkedObjects=DataGridFieldFactory)
    dexteritytextindexer.searchable('linkedObjects_linkedObjects')


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
                alsoProvides(widget, IFormWidget)

class AddView(add.DefaultAddView):
    form = AddForm
    

class EditForm(edit.DefaultEditForm):
    template = ViewPageTemplateFile('exhibition_templates/edit.pt')
    
    def update(self):
        super(EditForm, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                alsoProvides(widget, IFormWidget)

