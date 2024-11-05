from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Load tokenizer and model
model_name = "google/pegasus-cnn_dailymail"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

# Input text to summarize
input_text = """
Sarah – Hi Michael, is that you?

Michael – Hey Sarah! It’s been a while. How are things going?

Sarah – I’m doing well, thanks for asking. I just wrapped up a big project at work. How about you?

Michael – I’m doing well too. I recently moved to a new city for a job opportunity. It’s been quite an adjustment.

Sarah – That sounds exciting! What kind of job are you doing?

Michael – I’m working as a marketing strategist for a tech startup. It’s been a great experience so far, though challenging.

Sarah – That sounds really interesting. I’ve been working in event management for a couple of years now. It keeps me busy!

Michael – Event management must be a lot of fun. Do you get to work on any big events?

Sarah – Yes, quite a few. Just last month, I organized a major conference for a client. It was hectic but rewarding.

Michael – Wow, that sounds impressive. We should catch up in person and talk more about what we’ve been up to.

Sarah – I’d love that. Let’s find a time to meet up soon.

Michael – Definitely. I’ll check my schedule and get back to you.

Sarah – Great. Looking forward to it. Bye for now!

Michael – Bye! Take care.
"""

# Tokenize input text
tokens = tokenizer(input_text, truncation=True, padding="longest", return_tensors="pt")

# Generate summary
summary = model.generate(**tokens)

# Decode summary
decoded_summary = tokenizer.decode(summary[0], skip_special_tokens=True)
print("Summary:", decoded_summary)
