import nltk
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')

text = "This is a sample sentence! With, punctuation... and special characters \u00e2\u0080\u009c"

# Tokenize the text into words
words = word_tokenize(text)

# Filter out punctuation using string punctuation and create a new list of words without punctuation
filtered_words = [word for word in words if word not in string.punctuation]

print(filtered_words)
