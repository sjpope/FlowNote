from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os
""" Load GPT-2 Model and Tokenizer Globally """

tokenizer = GPT2Tokenizer.from_pretrained('D:/gpt2-large')
model = GPT2LMHeadModel.from_pretrained('D:/gpt2-large')