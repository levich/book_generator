from utils import BaseStructureChain, ChatOllama
from config import settings

MODEL = settings["model"]


class TitleChain(BaseStructureChain):

    PROMPT = settings["title.prompt"]

    def run(self, subject, genre, style, profile):
        return self.chain.predict(
            subject=subject, genre=genre, style=style, profile=profile
        )


class FrameworkChain(BaseStructureChain):

    PROMPT = settings["framework.prompt"]

    HELPER_PROMPT = settings["framework.helper_prompt"]

    def run(self, subject, genre, style, profile, title):

        features = ChatOllama(model=MODEL, base_url=settings["baseurl"]).predict(
            self.HELPER_PROMPT
        )

        framework = self.chain.predict(
            features=features,
            subject=subject,
            genre=genre,
            style=style,
            profile=profile,
            title=title,
        )

        return framework


class ChaptersChain(BaseStructureChain):

    PROMPT = settings["chapters.prompt"]

    def run(self, subject, genre, style, title, profile, framework):
        response = self.chain.predict(
            subject=subject,
            genre=genre,
            style=style,
            title=title,
            profile=profile,
            framework=framework,
        )
        print("**********************************************************************")
        print(response)
        print("**********************************************************************")
        return self.parse(response)

    def parse(self, response):
        chapter_list = response.strip().split("\n")
        chapter_list = [chapter for chapter in chapter_list if ":" in chapter]
        print("**********************************************************************")
        print([chapter.strip().split(":") for chapter in chapter_list])
        print("**********************************************************************")
        chapter_dict = dict(
            [chapter.strip().split(":", maxsplit=1) for chapter in chapter_list]
        )

        return chapter_dict


def get_structure(subject, genre, style, profile):
    title_chain = TitleChain()
    framework_chain = FrameworkChain()
    chapters_chain = ChaptersChain()
    print(settings['outfile'])
    if settings["title.load_title"]:
        title=settings["title.title"]
    else:
        title = title_chain.run(subject, genre, style, profile)

    print(title)

    if settings["framework.load_framework"]:
        framework=settings["framework.framework"]
    else:
        framework = framework_chain.run(subject, genre, style, profile, title)
    
    if settings["chapters.load_chapters"]:
        chapter_dict=settings["chapters_list"]
    else:
        chapter_dict = chapters_chain.run(subject, genre, style, profile, title, framework)

    return title, framework, chapter_dict
