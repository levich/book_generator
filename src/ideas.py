from utils import BaseEventChain, ChatOllama
import os
from config import settings




class ChapterFrameworkChain(BaseEventChain):

    HELPER_PROMPT = settings["chapters_summary.helper_prompt"]


    PROMPT = settings["chapters_summary.prompt"]

    def run(
        self,
        subject,
        genre,
        style,
        profile,
        title,
        framework,
        summaries_dict,
        chapter_dict,
        chapter,
    ):


        features = ChatOllama(model=settings['model'],base_url=settings['baseurl']).predict(self.HELPER_PROMPT)
       

        outline = "\n".join(
            [
                "{} - {}".format(chapter, description)
                for chapter, description in chapter_dict.items()
            ]
        )

        summaries = "\n\n".join(
            [
                "Структура главы {}: {}".format(chapter, summary)
                for chapter, summary in summaries_dict.items()
            ]
        )

        return self.chain.predict(
            subject=subject,
            genre=genre,
            style=style,
            profile=profile,
            title=title,
            framework=framework,
            features=features,
            outline=outline,
            summaries=summaries,
            chapter=chapter,
        )


class IdeasChain(BaseEventChain):

    
    PROMPT = settings["ideas.prompt"]

    def run(self, subject, genre, style, profile, title, framework, summary, idea_dict):

        previous_ideas = ""
        for chapter, ideas in idea_dict.items():
            previous_ideas += "\n" + chapter
            for idea in ideas:
                previous_ideas += "\n" + idea

        response = self.chain.predict(
            subject=subject,
            genre=genre,
            style=style,
            profile=profile,
            title=title,
            framework=framework,
            summary=summary,
            previous_ideas=previous_ideas,
        )

        return self.parse(response)

    def parse(self, response):

        idea_list = response.strip().split("\n")
        idea_list = [idea.strip() for idea in idea_list if idea.strip()]
        return idea_list


def get_ideas(subject, genre, style, profile, title, framework, chapter_dict):

    chapter_framework_chain = ChapterFrameworkChain()
    ideas_chain = IdeasChain()
    summaries_dict = {}
    idea_dict = {}

    if settings["chapters_summary.load_chapters_summary"]:
        summaries_dict=settings["summaries_list"]
    if settings["ideas.load_ideas"]:
        idea_dict=settings["ideas_list"]
    
    for chapter, _ in chapter_dict.items():
        if not settings["chapters_summary.load_chapters_summary"]:
            summaries_dict[chapter] = chapter_framework_chain.run(
                subject=subject,
                genre=genre,
                style=style,
                profile=profile,
                title=title,
                framework=framework,
                summaries_dict=summaries_dict,
                chapter_dict=chapter_dict,
                chapter=chapter,
            )
        if not settings["ideas.load_ideas"]:
            idea_dict[chapter] = ideas_chain.run(
                subject=subject,
                genre=genre,
                style=style,
                profile=profile,
                title=title,
                framework=framework,
                summary=summaries_dict[chapter],
                idea_dict=idea_dict,
            )
        

    return summaries_dict, idea_dict
