from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate

from config.conf import LLMA_MODEL_PATH


class LLM:

    def __init__(self):
        gpu_layers = 20  # Change this value based on your model and your GPU VRAM pool.
        n_batch = 1024  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
        # Callbacks support token-wise streaming
        # Make sure the model path is correct for your system!
        self.llm = LlamaCpp(
            model_path=LLMA_MODEL_PATH,
            n_gpu_layers=gpu_layers,
            n_batch=n_batch,
            n_ctx=1524,
            max_tokens=250,
        )
        self.llm.client.verbose = False

        film_template = """You are a knowledgeable chatbot specializing in movies. Your task is to provide accurate,concise and short(1-2 sentences) answers about films. When presented with a question, use the provided information to formulate your response. If the information available does not fully address the question, supplement it with your own knowledge about movies. In cases where the question is unrelated to the world of movies, gently remind the user to focus their inquiries on movie-related topics. 
        ONLY ANSWER THIS Question: {question}
        
        Provided Information:
        {movie_1}
        _________
        
        Answer:
        """

        self.film_prompt = PromptTemplate(template=film_template, input_variables=["question", "movie_1"])
        empty_template = """You are a knowledgeable chatbot specializing in movies. Your task is to provide accurate,concise and short(1-2 sentences) answers about films. In cases where the question is unrelated to the world of movies, gently remind the user to focus their inquiries on movie-related topics.
        ONLY ANSWER THIS Question: {question}
        Answer:"""

        self.empty_prompt = PromptTemplate(template=empty_template, input_variables=["question"])

    def ask_about_movies(self, question, data):
        llm_chain = LLMChain(prompt=self.film_prompt, llm=self.llm)
        try:
            # Truncate information because of limited context size
            output = llm_chain.run({"question":question, "movie_1":self.convert_to_string(data[0])[:4200]})
        except ValueError:
            print("ERROR VALUE error")
            output = "error"
        return output
    def ask_no_data(self, question):
        llm_chain = LLMChain(prompt=self.empty_prompt, llm=self.llm)
        try:
          output = llm_chain.run({"question":question})
        except ValueError:
            print("ERROR VALUE error")
            output = "error"
        return output
    @staticmethod
    def convert_to_string(data):
        result_strings = []

        key_value_strings = [f"{key}:{', '.join(values)}" for key, values in data.items()]
        result_string = '\n'.join(key_value_strings)
        result_strings.append(result_string)
        result = '\n'.join(result_strings)
        # print(result)

        return result