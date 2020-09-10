from collections import Counter
import re
import math


def get_jaccard_sim(arg1, arg2):
    a = set(arg1.split())
    b = set(arg2.split())
    c = a.intersection(b)
    return round(float(len(c)) / (len(a) + len(b) - len(c)), 3)


def get_cosine_similarity(arg1, arg2):
    counter1 = Counter(arg1.split())
    counter2 = Counter(arg2.split())
    terms = set(counter1).union(counter2)
    dotprod = sum(counter1.get(z, 0) * counter2.get(z, 0) for z in terms)
    mag1 = math.sqrt(sum(counter1.get(z, 0)**2 for z in terms))
    mag2 = math.sqrt(sum(counter2.get(z, 0)**2 for z in terms))
    return dotprod / (mag1 * mag2)


if __name__ == "__main__":
    str1 = "Hello how are you?"
    str2 = "hello I am fine, how are you!"
    # In this case we compare two strings while considering case sensitivity
    print(f"Case-sensitive Jaccard Similarity is: {get_jaccard_sim(str1, str2)}\n")
    print(f"Case-sensitive Cosine Similarity is: {get_cosine_similarity(str1, str2)}\n")
    # In this case we compare two strings case insensitive
    low_str1 = str1.lower()
    low_str2 = str2.lower()
    print(f"Case-insensitive Jaccard Similarity is: {get_jaccard_sim(low_str1, low_str2)}\n")
    print(f"Case-insensitive Cosine Similarity is: {get_cosine_similarity(low_str1, low_str2)}\n")
    # Comparing two case-insensitive strings by removing all the punctuations and special characters
    reg_str1 = re.sub('\W+', ' ', low_str1)
    reg_str2 = re.sub('\W+', ' ', low_str2)
    print(f"Case-insensitive string without punctuations and special characters Jaccard Similarity is: "
          f"{get_jaccard_sim(reg_str1, reg_str2)}\n")
    print(f"Case-insensitive string without punctuations and special characters Cosine Similarity is: "
          f"{get_cosine_similarity(reg_str1, reg_str2)}\n")
    # Jaccard Similarity takes only unique set of words for each sentence/document while cosine similarity takes
    # total length of the vectors. Ex: If you repeat the word "hello" in first string, cosine similarity changes,
    # but jaccard similarity does not
    rep_str1 = reg_str1 + " hello"
    rep_str2 = reg_str2
    print(f"Case-insensitive string without punctuations and special characters Jaccard Similarity is: "
          f"{get_jaccard_sim(rep_str1, rep_str2)}\n")
    print(f"Case-insensitive string without punctuations and special characters Cosine Similarity is: "
          f"{get_cosine_similarity(rep_str1, rep_str2)}\n")
    # Jaccard similarity is good for cases where duplication does not matter,
    # cosine similarity is good for cases where duplication matters while analyzing text similarity.
    # Common use case:
    # i)  Plagiarism: the cosine similarity would be ideal for plagiarism but jaccard similarity
    #    would not be appropriate
    # ii) Mirror Sites: the jaccard similarity would be ideal for determining mirror sites instead of cosine similarity
