from utils import BaseStructureChain,  ChatOllama
import os
from config import settings
MODEL=settings["model"]

class TitleChain(BaseStructureChain):
    # PROMPT = """
    # Your job is to generate a suitable title for a book about the following subject.
    # Please return a title and only a title!
    # The title should be consistent with the profile of the book.
    # The title should match the genre of the book.
    # The title should fit the style of the book.

    # Subject of the book: {subject}
    # Genre of the book: {genre}
    # Style: {style}

    # Profile of the book: {profile}

    # Title:"""

    PROMPT = settings["title.prompt"]

    def run(self, subject, genre, style, profile):
        return self.chain.predict(
            subject=subject, genre=genre, style=style, profile=profile
        )


class FrameworkChain(BaseStructureChain):
    # PROMPT = """
    # Your job is to generate the framework for a non-fiction book.
    # Return a framework and only a framework!
    # Describe the whole framework such that it serves as a roadmap for the book 
    # to organize its thoughts, present its arguments coherently, and guide the reader 
    # through the exploration of the book's central themes and concepts.
    # You are provided with the following subject, genre, style, title, and the profile of the book.
    # The frame work shoud be consistent with the profile of the book.
    # The framework should fit the genre of the book.
    # The framework should be compatible with the style of the book.

    # Consider the following attributes to write a comprehensive framework:
    # {features}

    # subject: {subject}
    # genre: {genre}
    # style: {style}
    # title: {title}
    # Profile of the book: {profile} 

    # framewrok:"""

    PROMPT = """
    Ваша задача - создать структуру для научно-популярного практического руководства (книги).
    Верните структуру и только структуру!
    Опишите всю структуру таким образом, чтобы она служила дорожной картой для книги
    , помогала систематизировать мысли, связно излагать аргументы и направлять читателя
    в изучении центральных тем и концепций книги.
    Вам будут предоставлены сведения о теме, жанре, стиле, названии и профиле книги.
    Структура должна соответствовать профилю книги.
    Структура должна соответствовать жанру книги.
    Структура должна соответствовать стилю книги.

    Учитывайте следующие атрибуты, чтобы создать всеобъемлющую структуру:
    {features}

    тема: {subject}
    жанр: {genre}
    стиль: {style}
    название: {title}
    Описание книги: {profile}

    Стуктура:"""

    # HELPER_PROMPT = """
    # Generate a list of attributes that characterizes a thought-provoking philosophical non-fiction book.
    
    # List of attributes:"""

    HELPER_PROMPT = """
    Составьте список характеристик, которые помогают написать научно-популярную книгу.
    
    Список характеристик:"""

    def run(self, subject, genre, style, profile, title):

        # features = ChatAnthropic(model_name="claude-3-opus-20240229").predict(self.HELPER_PROMPT)
        # features = ChatOpenAI(model="gpt-4-0125-preview").predict(self.HELPER_PROMPT)
        # features = ChatOpenAI(model="gpt-3.5-turbo-16k").predict(self.HELPER_PROMPT)
        features = ChatOllama(model=MODEL,base_url="http://172.26.24.195:11434/").predict(self.HELPER_PROMPT)
        # features = ChatOllama(model="mistral-openorca:latest").predict(self.HELPER_PROMPT)

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

    # PROMPT = """
    # Your job is to generate a list of chapters for a book.
    # Please generate the list of chapters and only the list of chapters!
    # You are provided with the subject, genre, style, title, profile, and the framework of the book.
    # Please generate a list of chapters that well describes the provided framework.
    # The chapter list should be consistent with the framework.
    # The chapter list should be according to the genre of the book.
    # The chapter list should follow the style of the book.
    # To generate the list of chapters, please follow the following template:

    # Introduction: [description of the introduction]
    # Chapter 1: [description of chapter 1]
    # ...
    # Afterword: [description of afterword]

    # Please make sure `Introduction` and `Afterword` have descriptions! Don't leave their description as empty spaces!
    # Please make sure each chapter is followed by the character `:` and its description.
    # Please generate one and only one description for each chapter. 
    # Do NOT break the chapter descriptions into multiple bullets! 
    # For example `Chapter 1: [description of chapter 1]`.

    # subject: {subject}
    # genre: {genre}
    # style: {style}
    # title: {title}
    # Profile of the book: {profile}
    # framework: {framework}

    # Please return the chapter list and only chapter list:"""

    PROMPT = """
    Ваша задача - создать список глав для книги.
    Пожалуйста, создайте список глав и только список глав!
    Вам будет предоставлена информация о теме, жанре, стиле, названии, профиле и структуре книги.
    Пожалуйста, составьте список глав, который хорошо описывает предлагаемую структуру.
    Список глав должен соответствовать структуре.
    Список глав должен соответствовать жанру книги.
    Список глав должен соответствовать стилю книги.
    Чтобы сформировать список глав, пожалуйста, следуйте следующему шаблону:

    Введение: [описание введения]
    Глава 1: [описание главы 1]
    ...
    Заключение: [описание послесловия]

    Пожалуйста, убедитесь, что в разделах "Введение` и `Заключение` есть описания! Не оставляйте их в виде пустых мест!
    Пожалуйста, убедитесь, что за каждой главой следует символ ":" и далее ее описание.
    Пожалуйста, создайте одно и только одно описание для каждой главы. 
    НЕ разбивайте описания глав на несколько разделов! 
    Например, "Глава 1: [описание главы 1]".

    тема: {subject}
    жанр: {genre}
    стиль: {style}
    название: {title}
    Описание книги: {profile}
    Структура книги: {framework}

    Пожалуйста, верните список глав и только список глав:"""

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
        chapter_dict = dict([chapter.strip().split(":",maxsplit=1) for chapter in chapter_list])

        return chapter_dict


def get_structure(subject, genre, style, profile):

    title_chain = TitleChain()
    framework_chain = FrameworkChain()
    chapters_chain = ChaptersChain()

    title = title_chain.run(subject, genre, style, profile)
    print(title)
    framework = framework_chain.run(subject, genre, style, profile, title)
    chapter_dict = chapters_chain.run(subject, genre, style, profile, title, framework)

    return title, framework, chapter_dict
