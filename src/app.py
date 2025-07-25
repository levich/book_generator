from collections import OrderedDict
import toml

from config import settings
from dynaconf import Dynaconf


MODEL=settings['model']

from structure import get_structure
from ideas import get_ideas
from writing import write_book
from publishing import DocWriter

subject = settings['subject']
profile = settings['profile']
style = settings['style']
genre = settings["genre"]

print(settings['outfile'])
doc_writer = DocWriter()

#создание структуры и содержания книги
title, framework, chapter_dict = get_structure(subject, genre, style, profile)
outdict = {}
outdict["title"]=title
outdict["style"]=style
outdict["genre"]=genre
outdict["profile"]=profile
outdict["subject"]=subject
outdict["framework"]=framework
outdict["chapters"]=chapter_dict


filename = settings["outfile"] if settings["outfile"] != "" else "out.toml"

with open(filename,"w",encoding="utf-8") as f:
    toml.dump(outdict,f)

#Создание суммарной информации по главам и списка идей для глав
summaries_dict, idea_dict = get_ideas(
    subject, genre, style, profile, title, framework, chapter_dict
)


outdict["summaries"]=summaries_dict
outdict["ideas"]=idea_dict

with open(filename,"w",encoding="utf-8") as f:
    toml.dump(outdict,f)

if settings["write_text"]:
    book = write_book(genre, style, profile, title, framework, summaries_dict, idea_dict)

    outdict["book"]=book
    with open(filename,"w",encoding="utf-8") as f:
        toml.dump(outdict,f)

    doc_writer.write_doc(book, chapter_dict, title)


doc_writer.write_structure(title,chapter_dict,summaries_dict,idea_dict)
