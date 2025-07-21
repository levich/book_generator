from collections import OrderedDict
import toml
from dynaconf import Dynaconf

from structure import get_structure
from ideas import get_ideas
from writing import write_book
from publishing import DocWriter



for b in range(1,10):


    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=['base.toml',f'settings.{b}.toml', '.secrets.toml'],
    )

    print(f"START PRODUCING BOOK {b}")

    MODEL=settings['model']





    subject = settings['subject']
    profile = settings['profile']
    style = settings['style']
    genre = settings["genre"]

    print(MODEL)
    doc_writer = DocWriter(settings)

    #создание структуры и содержания книги
    title, framework, chapter_dict = get_structure(settings,subject, genre, style, profile)
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
        settings, subject, genre, style, profile, title, framework, chapter_dict
    )


    outdict["summaries"]=summaries_dict
    outdict["ideas"]=idea_dict

    with open(filename,"w",encoding="utf-8") as f:
        toml.dump(outdict,f)

    if settings["write_text"]:
        book = write_book(settings, genre, style, profile, title, framework, summaries_dict, idea_dict)

        outdict["book"]=book
        with open(filename,"w",encoding="utf-8") as f:
            toml.dump(outdict,f)

        doc_writer.write_doc(book, chapter_dict, title)


    doc_writer.write_structure(title,chapter_dict,summaries_dict,idea_dict)
