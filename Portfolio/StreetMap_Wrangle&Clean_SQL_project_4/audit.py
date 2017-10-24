# coding: utf-8
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from num2words import num2words

OSMFILE = "Detroit.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
Street_numline_re = re.compile(r'\d0?(st|nd|rd|th|)\s(Line)$', re.IGNORECASE) 
# Spell lines ten and under
nth_re = re.compile(r'\d\d?(st|nd|rd|th|)', re.IGNORECASE)
nesw_re = re.compile(r'\s(North|East|South|West)$')

expected = ["Street", "Avenue", "Boulevard", "Parkway", "Drive", "Court", "Place", "Square", "Lane", "Road", "Trail",  "Commons", "Circle", "Crescent", "Gate", "Grove", "Way"]
mapping = {
            "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Dr.": "Drive",
            "Dr": "Drive",
            "Rd": "Road",
            "Rd.": "Road",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Trl": "Trail",
            "Cir": "Circle",
            "Cir.": "Circle",
            "Ct": "Court",
            "Ct.": "Court",
            "Crt": "Court",
            "Crt.": "Court",
	    "W.": "West",
            "W": "West",
            "N.": "North",
            "N": "North",
            "E.": "East",
            "E": "East",
            "S.": "South",
            "S": "South",
}

streetmapping = {
                   "St": "Street",
    		       "Rd": "Road",
                   "Rd.": "Road",
                   "St.": "Street",
                   "ST": "Street",
                   "Ave": "Avenue",
                   "Ave.": "Avenue",
                   "Rd.": "Road",
                   "Dr.": "Drive",
                   "Dr": "Drive",
                   "Blvd": "Boulevard",
                   "Blvd.": "Boulevard",
                   "Trl": "Trail",
                   "Cir": "Circle",
                   "Cir.": "Circle",
                   "Ct": "Court",
                   "Ct.": "Court",
                   "Crt": "Court",
                   "Crt.": "Court",
                }

number_mapping = {
                     "1st": "First",
                     "2nd": "Second",
                     "3rd": "Third",
                     "4th": "Fourth",
                     "5th": "Fifth",
                     "6th": "Sixth",
                     "7th": "Seventh",
                     "8th": "Eighth",
                     "9th": "Ninth",
                     "10th": "Tenth"
                   }


def audit_typestreet(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def check_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_typestreet(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name):

#Getting it clean for SQL

    if Street_numline_re.match(name):
        nth = nth_re.search(name)
        name = number_mapping[nth.group(0)]
        return name
    else:
        unchanged_name = name
        for key in mapping.keys():
            # check for names to replace i.e. Rd. to Road
            type_fix_name = re.sub(r'\s' + re.escape(key) + r'$', ' ' + mapping[key], unchanged_name)
            nesw = nesw_re.search(type_fix_name)
            if nesw is not None:
                for key in streetmapping.keys():
                    # Do not correct names like St. Anthony Blvd
                    dir_fix_name = re.sub(r'\s' + re.escape(key) + re.escape(nesw.group(0)), " " + streetmapping[key] + nesw.group(0), type_fix_name)
                    if dir_fix_name != type_fix_name:
                        # print unchanged_name + "=>" + type_fix_name + "=>" + dir_fix_name
                        return dir_fix_name
            if type_fix_name != unchanged_name:
                # return unchanged_name + "=>" + type_fix_name
                return type_fix_name
    # Look to see if road names are capitalized
    last_word = unchanged_name.rsplit(None, 1)[-1]
    if last_word.islower():
        unchanged_name = re.sub(last_word, last_word.title(), unchanged_name)
    return unchanged_name
