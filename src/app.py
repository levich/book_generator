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

# MODEL="gemma3:12b"
MODEL=os.getenv("MODEL")

from structure import get_structure
from ideas import get_ideas
from writing import write_book
from publishing import DocWriter



# subject = """
# The subject of the book is the intersection of AI and Philosophy. 
# This includes exploring philosophical questions arising from AI technology, 
# examining ethical implications, discussing the nature of intelligence, consciousness, 
# agency, and autonomy in AI systems, and considering the impact of AI on society, 
# culture, and human existence.
# """
subject = """
Тема книги - практическое руководство для специалистов в нефтепереработке по поиску задач для проектов машинного обучения и их успешного решения.
Основная цель книги - сделать из читателя квалифицированного заказчика проекта по машинному обучению. Она дает понимание как искать задачи для искусственного интеллекта, как внедрять такие проекты в нефтепереработку
и какие шаги следует сделать для получения успешного рзультата.
Также она включает основные риски и подводные камни в таких проектах и способы их избежать.
Также книга дает развернутое представление о том как оценивать эффективность проектов на основе машинного обучения и искусственного интеллекта.
Она включает в себя основные сведения по машинному обучению и искусственному интеллекту. Также книга включает в себя множество практических советов и подходов для поиска задач,
подходов к написанию технического задания, приемки результатов и внедрения технологий машинного обучения и искуственного интеллекта в нефтепереработку.
Книга включает вопросы на самопроверку и список конкретных рекомендуемых действий для читателя после каждой главы.
Также книга включает приложения содержащее основные термины из машинного обучения и искусственного интеллекта а также шаблон технического задания на проект на основе машинного обучения"""

# profile = """
# This interdisciplinary book aims to provide a comprehensive exploration of the philosophical 
# dimensions of artificial intelligence (AI) for a diverse audience interested in both AI and 
# philosophy. It targets academics, researchers, students of philosophy or computer science, 
# professionals in AI development, and general readers intrigued by the societal implications of AI. 
# By bridging the gap between philosophy and AI, the book delves into key themes such as ethics and morality, 
# consciousness and agency, epistemology and knowledge, and socio-cultural impacts. Through an interdisciplinary 
# approach drawing from philosophy, cognitive science, computer science, psychology, and sociology, each chapter 
# offers historical context, theoretical frameworks, current research findings, and speculative considerations 
# for the future, fostering critical thinking and informed discourse on the ethical and societal implications of AI.
# """

profile = """
Эта книга представляет из себя практическое руководство для специалистов нефтепереработки по выбору задачи, формированию корректного и всестороннего технического задания,
 контроля хода проекта, приемки результатов, внедрения и оценки экономического эффекта.
Основная аудитория книги - специалисты нефтепереработки, от операторов и начальников установок до руководителей нефтеперерабатывающих производств. Читатели - не специалисты в области 
искусственного интеллекта и машинного обучения. Они специалисты в области нефтепереработки.
Она дает все необходимые знания для квалифицированного заказчика проектов на основе машинного обучения. Книга включает в себя основные сведения об алгоритмах искусственного интеллекта, 
подходов к решению различных задач и способов оценки качества полученного результата.
Также книга показывает основные проблемы при реализации таких проектов - данные, интеграция, неуспешные внедрения и т.д., и предлагает способы решения этих проблем.
Книга дает детальный, пошаговый план поиска задачи, формирования технического задания, эффективной и прозрачной коммуникации со специалистами по искусственному интеллекту, приемке результата, 
оценки качества моделей и внедрения проекта в производство.
Она содержит объяснения основных терминов искусственного интеллекта для эффективной коммуникации со специалистами по машинному обучению.
Также она содержит в каждой главе список конкретных шагов, которые может сделать читатель после прочтения главы а также список вопросов для самопроверки.
В приложениях к книге содержится шаблон технического задания на проект машинного обучения, который по мере прочтения книги читатель может успешно заполнить.
Также в приложениях к книге содержится список интересных и полезных терминов и ссылок для читателя который хочет глубже погрузится в тему.
"""

style = "Analytical-Speculative-Historical"
style = "Практическое руководство-Компьютерные технологии-Искусственный интеллект"

genre = "Non-fiction: Philosophy of Technology/Science"
genre = "Научная литература: Искусственный интеллект и машинное обучение"
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

# book = write_book(genre, style, profile, title, framework, summaries_dict, idea_dict)

# doc_writer.write_doc(book, chapter_dict, title)
