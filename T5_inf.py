import transformers 
from transformers import T5ForConditionalGeneration, T5Tokenizer
from timeit import default_timer as timer

class T5Inference:
    def __init__(self, model_dir ="T5_offline_model"):

        self.model = T5ForConditionalGeneration.from_pretrained(model_dir)
        self.tokenizer = T5Tokenizer.from_pretrained(model_dir)
        self.prompt = ""


    def generate_answer(self, context, prompt):

        input_text = f"Context: {context} \nPrompt: {prompt}"
        input_ids = self.tokenizer(input_text, return_tensors ='pt').input_ids
        outputs = self.model.generate(input_ids,
                                      max_length = 30,
                                      num_beams = 5,
                                      early_stopping = True)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens = True)
        print(answer) # task: navigation, person_name: Prof. Morozov, destination_room: none
        parsed_answer = self.parse_answer(answer) # {'task': 'navigation', 'name': 'Prof. Morozov', 'room': 'none'}
        return parsed_answer
    
    
    def parse_answer(self, answer):
        # format the answer in dictionary form 
        # Initialize a dictionary with default values
        info_dict = {"task": None, "name": None, "room": None}

        # Split the answer string by comma and then by ': ' to extract key-value pairs
        parts = answer.split(", ")
        for part in parts:
            key_value = part.split(": ")
            if len(key_value) == 2:
                key, value = key_value
                key = key.strip().lower()  # Normalize keys to lowercase
                value = value.strip().lower()
                if key == "task":
                    info_dict["task"] = value
                elif key == "person_name":
                    info_dict["name"] = value
                elif key == "destination_room":
                    info_dict["room"] = value

        return info_dict

    
if __name__ == "__main__":
    start = timer()
    context = "I am here to meet Ms. Britta Lenz. can you help me find her? "
    prompt = """Can you read the text and identify the task, the destination room (if mentioned), and the person's name (if mentioned)? 
                If the destination room or the person's name is not mentioned, please specify 'none'. And, if the text says to avoid the first 
                mentioned name and room number and provides a second name or room number or both, only focus on the second name and room number."  
                """
    t5 = T5Inference()
    answer = t5.generate_answer(context=context, prompt=prompt)
    elapsed_time = timer() - start
    print(answer)
    print(elapsed_time)
