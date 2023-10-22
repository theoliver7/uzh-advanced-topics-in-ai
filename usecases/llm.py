from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate


class LLM:

    def __init__(self):
        gpu_layers = 29  # Change this value based on your model and your GPU VRAM pool.
        n_batch = 1024  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
        self.llm = LlamaCpp(
            model_path="/home/oliver/dev/uzh/atai_bot/orca-mini-3b-gguf2-q4_0.gguf",
            n_gpu_layers=gpu_layers,
            n_batch=n_batch,
            n_ctx=1024,
            verbose=True,  # Verbose is required to pass to the callback manager
        )

        template = """Answer the question with below information, Always answer in a sentence: {question}
        If possible answer with below information: 
        {movie_1}
        If this is not the asked movie check here: 
        {movie_2}
        Answer: """

        self.film_prompt = PromptTemplate(template=template, input_variables=["question", "movie_1", "movie_2"])

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

    @staticmethod
    def convert_to_string(data):
        result_strings = []  # List to hold the result strings for each dictionary

        # List comprehension to construct the "key:value" strings for each key-value pair
        key_value_strings = [f"{key}:{', '.join(values)}" for key, values in data.items()]
        # Join the "key:value" strings with a newline character to form the result string for this dictionary
        result_string = '\n'.join(key_value_strings)
        result_strings.append(result_string)
        # Separate the result strings for each dictionary with two newline characters
        result = '\n'.join(result_strings)
        return result