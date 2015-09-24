#!/usr/bin/python
# -*- coding: utf-8 -*-


from plone.indexer.decorator import indexer
from ..exhibition import IExhibition

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