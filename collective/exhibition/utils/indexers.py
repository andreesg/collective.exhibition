#!/usr/bin/python
# -*- coding: utf-8 -*-


from plone.indexer.decorator import indexer
from ..exhibition import IExhibition
from z3c.relationfield.interfaces import IRelationList, IRelationValue

@indexer(IExhibition)
def exhibition_organiser(object, **kw):
    try:
        if hasattr(object, 'exhibitionsDetails_organizingInstitution'):
            items = object.exhibitionsDetails_organizingInstitution
            organisers = []
            if items:
                for item in items:
                    if IRelationValue.providedBy(item):
                        organiser_obj = item.to_object
                        title = getattr(organiser_obj, 'title', "")
                        organisers.append(title)
                    elif getattr(item, 'portal_type', "") == "PersonOrInstitution":
                        title = getattr(item, 'title', "")
                        organisers.append(title)
                    else:
                        continue

            return "_".join(organisers)
        else:
            return ""
    except:
        return ""

@indexer(IExhibition)
def exhibitionsDetails_itinerary_place(object, **kw):
    try:
        if hasattr(object, 'exhibitionsDetails_itinerary'):
            terms = []
            items = object.exhibitionsDetails_itinerary
            if items:
                for item in items:
                    if item['place']:
                        for term in item['place']:
                            if term:
                                terms.append(term)

            return terms
        else:
            return []
    except:
        return []

@indexer(IExhibition)
def end(object, **kw):
    try:
        if hasattr(object, 'end'):
            return object.end
    except:
        return ""

@indexer(IExhibition)
def start(object, **kw): 
    try:
        if hasattr(object, 'start'):
            return object.start
    except:
        return ""

