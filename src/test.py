from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Укажите URL вашей удаленной Ollama instance.
# Убедитесь, что Ollama instance доступна по указанному адресу и разрешает входящие соединения.
OLLAMA_URL = "http://172.26.24.195:11434"  # Замените на ваш URL

# Создайте экземпляр LLM, указав URL
llm = Ollama(
    model="gemma3:27b",  # Или любая другая модель, установленная в вашей Ollama instance
    base_url=OLLAMA_URL,
)

# Создайте PromptTemplate
template = """
Answer the following question:

{question}
"""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Создайте LLMChain
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Задайте вопрос
question = "What is the capital of France?"

# Запустите цепочку и получите ответ
response = llm_chain.run(question)

# Выведите ответ
print(response)