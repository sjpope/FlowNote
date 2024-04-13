from transformers import GPT2LMHeadModel, GPT2Tokenizer

""" Load GPT-2 Model and Tokenizer Globally """

tokenizer = GPT2Tokenizer.from_pretrained('./tokenizer')
model = GPT2LMHeadModel.from_pretrained('./models')