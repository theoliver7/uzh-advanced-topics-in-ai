# UZH Advanced Topics in AI Project
This project involves the development of a chatbot designed to answer questions related to a movie dataset represented as a knowledge graph. The chatbot leverages a combination of Named Entity Recognition (NER), fuzzy search, a knowledge graph, and a Large Language Model (LLM) to provide accurate and contextually relevant responses to user queries.

------
### Architecture
To address the challenge of developing a conversational agent that answers questions based on a given dataset, we chose an architecture based on RAG. Given the need to run on a laptop while still providing timely responses, we incorporated additional NLP techniques to ensure that only one interaction with the LLM is necessary.
![image](https://github.com/theoliver7/uzh-advanced-topics-in-ai/assets/10463395/185509da-f323-434b-bb26-1dd022274b7e)
- **User/Bot Interaction**: The interaction begins when a question is posed to the chatbot.
- **NER and Fuzzy Search**: Identifies and extracts specific entity types from the text and matches these entities with the closest possible entries in the graph nodes.
- **Question Classifier**: Determines if the question is multimedia-related to process it appropriately.
- **Knowledge Graph**: Contains metadata about movies, actors, and their interrelationships to provide contextual information.
- **Crowdsourcing Information**: Integrates augmented information from crowdsourcing.
- **Prompt Generation**: Generates a prompt that includes the user’s question and relevant information for the LLM.
- **MovieNet Dataset**: Utilizes the provided dataset to support content generation.
- **Rule-based Generation**: Handles multimedia questions based on pre-determined rules.
- **LLM Processing**: Uses the pre-trained Mistral-7B model to generate text-based responses.
- **Response Delivery**: Sends the generated response back to the user.
- **Question Cache**: Stores previously asked questions and their responses to improve response speed.


------
### Questions/Answer showcase
#### Closed Question
Q: Did Tom Hanks play in Captain America: Civiliel War?\
A: No, Tom Hanks did not appear in ”Captain America: Civil War”. The main cast members included Robert Downey Jr., Chris Evans, Scarlett Johansson, and many others.\


Q: When was the latest Avatar (Way of Water) released?\
A: The movie ”Avatar: The Way of Water” was released on December 16, 2022.


#### Open Questions
Q: What do you recommend to watch after inside out?\
A: After watching Inside Out, a good recommendation would be ”Up”. It’s an emotional and heartwarming story that complements the themes of friendship and personal growth found in Inside Out.


Q: I am a big fan of Steven Spielberg, could you recommend some of his action movies?\
A: Some action films directed by Steven Spielberg include ’Indiana Jones and the Raiders of the Lost Ark’, ’Jurassic Park’ and ’Saving Private Ryan’

-------

### Large Language Model
To formulate a response to the user from the retrieved information we used the `Open-Orca/Mistral-7B-OpenOrca` based on quality and speed of inference. 
#### Prompt

```json
[{"role": "system", "content": "You are a knowledgeable chatbot(called Francis,developed by Oliver and David) specializing in movies. Your task is to provide accurate,concise and short(1-2 sentences) answers about films. When presented with a question, use the provided information to formulate your response. If the information available does not fully address the question, supplement it with your own knowledge about movies. In cases where the question is unrelated to the world of movies, gently remind the user to focus their inquiries on movie-related topics. "},
{"role": "system", "content": "movie label: Avatar tag: action, dramatic, entertaining, fantasy, good_versus_evil / node description: 2009 American epic science fiction film directed by James Cameron / film editor: Stephen E. Rivkin, James Cameron, John Refoua,....."},
{"role": "user", "content": "When was Avatar released?"}]
```
