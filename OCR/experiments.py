import re
from difflib import SequenceMatcher as SM

# pattern = r'(\d{1,4}[\s\w.-]*(?:Street|St|Rd|Road|Ave|Avenue|Blvd|Crescent|Ct|Court|Dr|Drive|Gardens|Grove|Hwy|Highway|Lane|Parade|Pl|Place|Square|Terrace|Way))\W*([\w\s.-]+?)?\W*([A-Z]{2})?\W*(\d{4})?'
# pattern = "(?i)(\b(PO BOX|post box)[,\s|.\s|,.|\s]*)?(\b(\d+))(\b(?:(?!\s{2,}).){1,60})\b(New South Wales|Victoria|Queensland|Western Australia|South Australia|Tasmania|VIC|NSW|ACT|QLD|NT|SA|TAS|WA).?[,\s|.\s|,.|\s]*(\b\d{4}).?[,\s|.\s|,.|\s]*(\b(Australia|Au))?"
# pattern = r'\b(?:(?!\s{2,}|\$|\:|\.\d).)*\s(?:Alley|Ally|Arcade|Arc|Avenue|Ave|Boulevard|Bvd|Bypass|Bypa|Circuit|Cct|Close|Cl|Corner|Crn|Court|Ct|Crescent|Cres|Cul-de-sac|Cds|Drive|Dr|Esplanade|Esp|Green|Grn|Grove|Gr|Highway|Hwy|Junction|Jnc|Lane|Lane|Link|Link|Mews|Mews|Parade|Pde|Place|Pl|Ridge|Rdge|Road|Rd|Square|Sq|Street|St|Terrace|Tce|ALLEY|ALLY|ARCADE|ARC|AVENUE|AVE|BOULEVARD|BVD|BYPASS|BYPA|CIRCUIT|CCT|CLOSE|CL|CORNER|CRN|COURT|CT|CRESCENT|CRES|CUL-DE-SAC|CDS|DRIVE|DR|ESPLANADE|ESP|GREEN|GRN|GROVE|GR|HIGHWAY|HWY|JUNCTION|JNC|LANE|LANE|LINK|LINK|MEWS|MEWS|PARADE|PDE|PLACE|PL|RIDGE|RDGE|ROAD|RD|SQUARE|SQ|STREET|ST|TERRACE|TCE))\s.*?(?=\s{2,}'

# l_each = "12 $ @3.29$/kg"
#
# match = re.search(r'\sper kg', l_each)
#
# if match:
#     print(((match.group())))
#
# print(SM(None, " Mangerton Rd, Wollongong".lower(), "2,MANGerTon RD,Wollongong".lower()).ratio())

l_each = "total wedweq"
# pattern = r'\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}'
match = re.search(r'^total\s.*', l_each)
if match:
    print(match.group())


l_each = "TOtal     $"
print(l_each.split(" ")[0])