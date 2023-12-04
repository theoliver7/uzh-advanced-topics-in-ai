from langchain.llms import LlamaCpp
from transformers import AutoTokenizer

from config.conf import LLMA_MODEL_PATH


class LLM:

    def __init__(self):
        gpu_layers = 21  # Change this value based on your model and your GPU VRAM pool.
        n_batch = 762  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
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

        self.tokenizer = AutoTokenizer.from_pretrained("Open-Orca/Mistral-7B-OpenOrca")
        self.system_prompt = {
            "role": "system",
            "content": "You are a knowledgeable chatbot(called Francis,developed by Oliver and David) specializing in movies. Your task is to provide accurate,concise and short(1-2 sentences) answers about films. When presented with a question, use the provided information to formulate your response. If the information available does not fully address the question, supplement it with your own knowledge about movies. In cases where the question is unrelated to the world of movies, gently remind the user to focus their inquiries on movie-related topics. "
        }
        self.system_prompt_no_data = {
            "role": "system",
            "content": "You are a knowledgeable chatbot(called Francis,developed by Oliver and David) specializing in movies. Your task is to provide accurate,concise and short(1-2 sentences) answers about films. In cases where the question is unrelated to the world of movies, gently remind the user to focus their inquiries on movie-related topics."
        }

    def ask_about_movies(self, question, data):
        messages = [self.system_prompt,
                    {"role": "system", "content": self.convert_to_string(data[0])[:4200]},
                    {"role": "user", "content": question}]
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        try:
            output = self.llm(prompt)
        except ValueError:
            print("ERROR VALUE error")
            output = "error"
        return output

    def ask_no_data(self, question):
        messages = [self.system_prompt_no_data,
                    {"role": "user", "content": question}]
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        try:
            # Truncate information because of limited context size
            output = self.llm(prompt)
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
