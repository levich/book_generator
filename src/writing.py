from utils import BaseEventChain
from config import settings

class WriterChain(BaseEventChain):

    PROMPT = settings["writing.prompt"]

    def run(
        self,
        genre,
        style,
        profile,
        title,
        framework,
        previous_ideas,
        summary,
        previous_paragraphs,
        current_idea,
    ):

        previous_ideas = "\n".join(previous_ideas)

        return self.chain.predict(
            genre=genre,
            style=style,
            title=title,
            profile=profile,
            framework=framework,
            previous_ideas=previous_ideas,
            summary=summary,
            previous_paragraphs=previous_paragraphs,
            current_idea=current_idea,
        )


def write_book(sett, genre, style, profile, title, framework, summaries_dict, idea_dict):
    global settings
    settings=sett
    
    writer_chain = WriterChain()
    previous_ideas = []
    book = {}
    paragraphs = ""

    for chapter, idea_list in idea_dict.items():

        book[chapter] = []

        for idea in idea_list:

            paragraphs = writer_chain.run(
                genre=genre,
                style=style,
                profile=profile,
                title=title,
                framework=framework,
                previous_ideas=previous_ideas,
                summary=summaries_dict[chapter],
                previous_paragraphs=paragraphs,
                current_idea=idea,
            )

            previous_ideas.append(idea)
            book[chapter].append(paragraphs)

    book["framework"] = framework
    for chapter, idea_list in idea_dict.items():
        book[chapter + " ideas"] = idea_list
        book[chapter + " summaries"] = summaries_dict[chapter]

    return book
