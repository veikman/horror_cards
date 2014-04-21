# -*- coding: utf-8 -*-

from cbg.elements import CardContentField as F
from cbg.tag import Tag as T
import cbg.card
import cbg.tag
import cbg.elements
import cbg.exc

import dresser

TITLE = F(cbg.card.TITLE, dresser.Title)
TAGS = cbg.tag.FieldOfTags('tags', dresser.Tagbox, T.all_)
LEAD = F('lead', dresser.Lead)
CRUNCH = F('crunch', dresser.Crunch)

BASIC = ( TITLE
        , TAGS
        , LEAD
        , CRUNCH
        )
