import logging
from .utils import preprocess_text, strip_html_tags, remove_prompt_from_content
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

from notes.models import Note, NoteGroup

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tokenizer = GPT2Tokenizer.from_pretrained('./tokenizer')
model = GPT2LMHeadModel.from_pretrained('./models')

def generate_content(prompt, max_length=150, num_return_sequences=2, additional_tokens=500):
    encoding = tokenizer(prompt, return_tensors='pt', truncation=True)
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    total_max_length = input_ids.shape[1] + additional_tokens

    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=total_max_length,
            min_length=input_ids.shape[1] + 20,  
            temperature=0.8, 
            top_k=50,
            top_p=0.92,
            no_repeat_ngram_size=3,  
            num_return_sequences=num_return_sequences,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    suggestions = [tokenizer.decode(generated_id, skip_special_tokens=True) for generated_id in generated_ids]
    return suggestions

def analyze(content):
    processed_content = preprocess_text(content)
    if len(processed_content.split()) < 25:
        logging.warning("Text too short for analysis.")
        return "Text too short for analysis."
    keywords = preprocess_and_extract_keywords(processed_content)
    summary = generate_content(f"Summarize this content: {content}", num_return_sequences=1)[0]
    cleaned_summary = remove_prompt_from_content(f"Summarize this content: {content}", summary)
    return {
        "keywords": ', '.join(keywords),
        "summary": cleaned_summary
    }
    
"""
TO-DO: ITERATE THROUGH THESE OLD FUNCTIONS AND KEEP WHAT'S NEEDED
"""

""" Auto Grouping Methods"""
def compute_similarity_matrix(contents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(contents)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def group_note(target_note, other_notes, similarities, threshold=0.5):
    similar_indices = np.where(similarities > threshold)[0] 
    similar_indices = [int(i) for i in similar_indices]
    similar_notes = [other_notes[i] for i in similar_indices]

    if similar_notes:
        note_group = NoteGroup(title=f"Group for Note {target_note.pk} - {now().strftime('%Y-%m-%d %H:%M:%S')}", owner=target_note.owner)
        note_group.save()
        note_group.notes.add(target_note, *similar_notes)
        return note_group
    
def group_all_notes(notes, similarity_matrix, threshold=0.5, owner=None):
    note_groups = []
    visited = set()

    for idx, similarities in enumerate(similarity_matrix):
        if idx in visited:
            continue

        similar_indices = [int(i) for i in np.where(similarities > threshold)[0]]
        group = [notes[i] for i in similar_indices if i not in visited]

        visited.update(similar_indices)

        if group:
            note_group = NoteGroup(
                title=f"Auto Group {len(note_groups) + 1} - {now().strftime('%Y-%m-%d %H:%M:%S')}",
                owner=owner 
            )
            note_group.save()
            note_group.notes.set(group)
            note_groups.append(note_group)

    return note_groups

""" Analysis Methods (Summary, Keywords)"""

# Create function to make sentence count dynamic based on input size.
# def summarize_text_with_lsa(text, sentence_count=3):
    
#     parser = PlaintextParser.from_string(text, Tokenizer("english"))
#     summarizer = LsaSummarizer()
#     summary = summarizer(parser.document, sentence_count)
#     summary_text = " ".join([str(sentence) for sentence in summary])
    
#     return summary_text

# def summarize_with_gpt2(note_content):
#     prompt = f"Summarize this content: {note_content}"
#     summary = generate_content_task(prompt, num_return_sequences=1)[0]
#     # Remove the original prompt from the summary to clean it up
#     cleaned_summary = remove_prompt_from_content(prompt, summary)
#     return cleaned_summary

# def summarize_with_gpt2(text, model, tokenizer):
#     # Ensure the text is clean and free from HTML tags
#     text = strip_html_tags(text)
    
#     # Craft a more concise prompt for summarization
#     prompt = "Summarize this content succinctly:"
#     inputs = tokenizer.encode_plus(prompt + text, return_tensors='pt', max_length=512, truncation=True)
    
#     # Generate summary with the updated parameters
#     summary_ids = model.generate(
#         inputs['input_ids'],
#         attention_mask=inputs['attention_mask'],
#         max_length=150,
#         min_length=40,
#         length_penalty=2.0,
#         num_beams=5,
#         no_repeat_ngram_size=2,
#         early_stopping=True,
#         pad_token_id=tokenizer.eos_token_id,
#         temperature=0.7,  # Adjust temperature for more deterministic output
#         top_k=50,  # Limits the number of highest probability vocabulary tokens considered for each step
#         top_p=0.95,  # Nucleus sampling: only considers the top p% of the cumulative probability distribution
#         do_sample=True  # Enable sampling to utilize temperature and top_p
#     )

#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary


# def analyze(content, model, tokenizer):
#     processed_notes = preprocess_text(content)  
#     logging.debug(f"Processed Notes: {processed_notes}")

#     if len(processed_notes.split()) < 25:
#         logging.warning("Text too short or insignificant for analysis.")
#         return "Text too short or insignificant for analysis."

#     keywords = preprocess_and_extract_keywords(processed_notes)
#     logging.info(f"Extracted Keywords: {keywords}")

#     # summary = summarize_text_with_lsa(processed_notes)
#     # logging.info(f"Summary (LSA): {summary}\n\n\n")
#     summary_gpt2 = ""
#     try:
#         summary_gpt2 = summarize_with_gpt2(content)
#         logging.info(f"Summary (GPT-2): {summary_gpt2}")
#     except Exception as e:
#         logging.error(f"Error in summarize_with_gpt2: {e}")
#         summary_gpt2 = "Error generating summary with GPT-2."
    
#     keywords_str = ', '.join(keywords)  
#     analysis_result = f"Keywords: {keywords_str}\n\nSummary: {summary_gpt2}"
    
#     return analysis_result

