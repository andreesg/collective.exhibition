#!/usr/bin/python
# -*- coding: utf-8 -*-

#from collective.leadmedia.adapters import ICanContainMedia
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from collective.exhibition import MessageFactory as _
from plone.dexterity.browser.view import DefaultView


from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent
from plone.app.z3cform.widget import AjaxSelectFieldWidget, AjaxSelectWidget, SelectWidget, DatetimeFieldWidget, IAjaxSelectWidget, RelatedItemsFieldWidget
from zope.interface import alsoProvides
from .interfaces import IFormWidget
from plone.dexterity.browser import add, edit
from collective.z3cform.datagridfield.interfaces import IDataGridField
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from Acquisition import aq_inner
from zc.relation.interfaces import ICatalog

# # # # # # # # # # # # #
# View specific methods #
# # # # # # # # # # # # #

class ExhibitionView(edit.DefaultEditForm):
    """ View class """

    template = ViewPageTemplateFile('../exhibition_templates/view.pt')

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
        super(ExhibitionView, self).update()
        for group in self.groups:
            for widget in group.widgets.values():
                if IDataGridField.providedBy(widget):
                    widget.auto_append = False
                    widget.allow_reorder = True
                alsoProvides(widget, IFormWidget)

        for widget in self.widgets.values():
            if IDataGridField.providedBy(widget) or IAjaxSelectWidget.providedBy(widget):
                widget.auto_append = False
                widget.allow_reorder = True
            alsoProvides(widget, IFormWidget)

    def checkUserPermission(self):
        sm = getSecurityManager()
        if sm.checkPermission(ModifyPortalContent, self.context):
            return True
        return False

    def showManageButton(self):
        secman = getSecurityManager()
        if not secman.checkPermission('Portlets: Manage portlets', self.context):
            return False
        else:
            return True
