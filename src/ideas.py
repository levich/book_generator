from utils import BaseEventChain, ChatOllama
import os
MODEL=os.getenv("MODEL")


class ChapterFrameworkChain(BaseEventChain):

    # HELPER_PROMPT = """
    # Generate a list of attributes that characterizes a thought-provoking philosophical non-fiction book, 
    # including a consistent chain of ideas, which support the main framework of the book.
    # List of attributes:"""
    HELPER_PROMPT = """
    Составьте список характеристик, которые характеризуют научно-популярное практическое руководство по машинному обучению и искусственному интеллекту для нефтепереработчиков, 
    дающее последовательное понимание как практически реализовать проект машинного обучения,
включая последовательную цепочку идей, которые поддерживают основную структуру книги.
    Список характеристик:"""

    # PROMPT = """
    # You are a writer and your job is to generate the framework for one and only one chapter of a philosophical non-fiction book. 
    # You are provided with the subject, genre, style, title, profile, and the main framework of the book. 
    # Additionally, you are provided with the framework of the previous chapters and the outline of the book.
    # Make sure to generate a framework that describes accurately the ideas and arguments of the chapter. 
    # Each chapter should have its own ideas and arguements, but should be consistent with 
    # the other chapters and the overall framework of the book.
    # The framework of the chapter should be consistent with the genre of the novel.
    # The framework of the chapter should be according to the style of the book. 

    # Consider the following attributes to write a stimulating and insightful book:
    # {features}

    # subject: {subject}
    # genre: {genre}
    # style: {style}
    # title: {title}
    # profile of the book: {profile}
    # framework: {framework}

    # Outline:
    # {outline}

    # Chapter Framework:
    # {summaries}

    # Return a detailled framework. DON'T refer to the title nor the chapter's name in the framework!
    # Return the framework and only the framework of the ideas and supporting arguements in the chapter.
    # Framework of {chapter}:"""
    PROMPT = """
    Вы писатель, и ваша задача - создать основу для одной-единственной главы практического руководства по машинному обучению и искуссвенному интеллекту для специалистов нефтепереработки. 
    Вам предоставляется тема, жанр, стиль, название, профиль и основные принципы книги. 
    Кроме того, вам предоставляется структура предыдущих глав и общий план книги.
    Убедитесь, что вы создали структуру, которая точно описывает идеи и аргументы, изложенные в главе. 
    В каждой главе должны быть свои собственные идеи и аргументы, но они должны соответствовать 
    другие главы и общая структура книги.
    Структура главы должна соответствовать жанру романа.
    Структура главы должна соответствовать стилю книги. 

    Чтобы написать увлекательную и содержательную книгу, обратите внимание на следующие характеристики:
    {features}

    тема: {subject}
    жанр: {genre}
    стиль: {style}
    название: {title}
    описание книги: {profile}
    фреймворк: {framework}

    Краткое изложение:
    {outline}

    Структура главы:
    {summaries}

    Верните подробную структуру. НЕ ссылайтесь на название главы в структуре!
    Верните структуру и только структуру идей и подтверждающих аргументов в главе.
    Структура {chapter}:"""

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

        # features = ChatAnthropic(model_name="claude-3-opus-20240229").predict(self.HELPER_PROMPT)
        # features = ChatOpenAI(model="gpt-4-0125-preview").predict(self.HELPER_PROMPT)
        # features = ChatOpenAI(model="gpt-3.5-turbo-16k").predict(self.HELPER_PROMPT)
        features = ChatOllama(model=MODEL,base_url="http://172.26.24.195:11434/").predict(self.HELPER_PROMPT)
        # features = ChatOllama(model="mistral-openorca:latest").predict(self.HELPER_PROMPT)

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

    # PROMPT = """
    # You are a philosophical writer and your job is to come up with a detailed list of ideas discussed 
    # in the current chapter of the book.
    # Be very specific about the supporting arguements and traits of the different ideas.
    # Those ideas describe the framework of that chapter and the supporting arguments of the different ideas
    #  should be in rigorous order. 
    # You are provided with the subject, genre, style, title, profile, and the main framework of the book, and 
    # also the framework of that chapter.
    # Additionally, you are provided with the list of the ideas that were outlined in the previous chapters.
    # The idea list should be consistent with the genre of the book.
    # The idea list should be consistent with the style of the book.

    # The each element of that list should be returned on different lines. Follow this template:

    # Idea 1
    # Idea 2
    # ...
    # Final idea

    # subject: {subject}
    # genre: {genre}
    # style: {style}
    # title: {title}
    # profile of the book: {profile}
    # framework: {framework}

    # Ideas you outlined for previous chapters: {previous_ideas}

    # Framework of the current chapter:
    # {summary}

    # Don't hesitate to create the necessary idaes to generate a meaningful framework.
    # Return the ideas and only the ideas that capture the framework!
    # Idea list for that chapter:"""

    PROMPT = """
    Вы пишете практическое руководство по машинному обучению для специалистов нефтепереработки и ваша задача - составить подробный список идей, обсуждаемых в текущей главе книги.
    Будьте предельно конкретны в отношении аргументации и особенностей различных идей.
    Все идеи описывающие структуру этой главы и аргументы, подтверждающие различные идеи должны быть в строгом порядке. 
    Вам предоставляется информация о теме, жанре, стиле, названии, профиле и основных принципах книги, а
    также о структуре этой главы.
    Кроме того, вам предоставляется список идей, которые были изложены в предыдущих главах.
    Список идей должен соответствовать жанру книги.
    Список идей должен соответствовать стилю книги.

    Каждый элемент этого списка должен отображаться в разных строках. Следуйте этому шаблону:

    Идея 1
    Идея 2
    ...
    Заключительная идея

    тема: {subject}
    жанр: {genre}
    стиль: {style}
    название: {title}
    описание книги: {profile}
    фреймворк: {framework}

    Идеи, которые вы изложили для предыдущих глав: {previous_ideas}

    Рамки текущей главы:
    {summary}

    Не стесняйтесь создавать необходимые идеи для создания значимой структуры.
    Возвращайте идеи, и только те идеи, которые укладываются в рамки!
    Список идей для этой главы:"""

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

    for chapter, _ in chapter_dict.items():

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
