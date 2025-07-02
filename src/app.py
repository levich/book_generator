from collections import OrderedDict
from dotenv import load_dotenv
import os
from yaml import load, dump,safe_dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from ruamel.yaml import YAML

load_dotenv()

from config import settings

print(settings['model'])

# MODEL="gemma3:12b"
MODEL=settings['model']

from structure import get_structure
from ideas import get_ideas
from writing import write_book
from publishing import DocWriter



subject = settings['subject']



profile = settings['profile']


style = settings['style']

genre = settings["genre"]

print(MODEL)
doc_writer = DocWriter()


title, framework, chapter_dict = get_structure(subject, genre, style, profile)
outdict = {}
outdict["title"]=title
outdict["style"]=style
outdict["genre"]=genre
outdict["profile"]=profile
outdict["subject"]=subject
outdict["framework"]=framework
outdict["chapters"]=chapter_dict






yaml = YAML(typ='unsafe', pure=True)


yaml.default_style="|"
yaml.allow_unicode=True

with open("out.yaml","w") as f:
    #dump_str = safe_dump(outdict,f, allow_unicode=True,default_style='|')
    yaml.dump(outdict,f)


summaries_dict, idea_dict = get_ideas(
    subject, genre, style, profile, title, framework, chapter_dict
)


outdict["summaries"]=summaries_dict
outdict["ideas"]=idea_dict

with open("out.yaml","w") as f:
    #dump_str = safe_dump(outdict,f, allow_unicode=True,default_style='|')
    yaml.dump(outdict,f)

book = write_book(genre, style, profile, title, framework, summaries_dict, idea_dict)

doc_writer.write_doc(book, chapter_dict, title)
