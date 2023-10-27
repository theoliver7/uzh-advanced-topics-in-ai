from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate


class LLM:

    def __init__(self):
        gpu_layers = 20  # Change this value based on your model and your GPU VRAM pool.
        n_batch = 1024  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
        # Callbacks support token-wise streaming
        # Make sure the model path is correct for your system!
        self.llm = LlamaCpp(
            model_path="/home/oliver/dev/uzh/atai_bot/mistral-7b-openorca.Q4_0.gguf",
            n_gpu_layers=gpu_layers,
            n_batch=n_batch,
            n_ctx=1524,
            verbose=True,  # Verbose is required to pass to the callback manager
        )

        film_template = """Answer the question with below information, Always answer in a sentence: {question}
        If possible answer with below information: 
        {movie_1}
        If this is not the asked movie check here: 
        {movie_2}
        Answer: """

        self.film_prompt = PromptTemplate(template=film_template, input_variables=["question", "movie_1", "movie_2"])
        empty_template = """Answer the question with below information, Always answer in a sentence: {question}
                Answer: """

        self.empty_prompt = PromptTemplate(template=empty_template, input_variables=["question"])

    def ask_about_movies(self, question, data):
        llm_chain = LLMChain(prompt=self.film_prompt, llm=self.llm)
        try:
            if len(data)==2:
                output = llm_chain.run({"question":question, "movie_1":self.convert_to_string(data[0]),"movie_2":self.convert_to_string(data[1])})
            else:
                output = llm_chain.run({"question":question, "movie_1":self.convert_to_string(data[0]),"movie_2":"No Info"})
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
        return result