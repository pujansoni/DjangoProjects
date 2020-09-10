from django.core.management import BaseCommand

from collections import Counter, OrderedDict
import re
import math
from tabulate import tabulate
from corona_world_statistics.models import CoronaStats, CoronaArticles


def get_jaccard_similarity(arg1, arg2):
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

def iterate_dictionary(dict):
    column_name = ['Record Id', 'Title', 'Abstract', 'Author', 'Journal/Publisher', 'Similarity Measure']
    list_of_records = []
    for key, value in dict.items():
        temp_list = []
        article = CoronaArticles.objects.get(pk=key)
        temp_list.append(article.id)
        temp_list.append('%.70s' % article.title)
        temp_list.append('%.13s' % article.abstract)
        temp_list.append('%.13s' % article.author)
        temp_list.append('%.13s' % article.journal_publisher)
        temp_list.append(value)
        list_of_records.append(temp_list)
    print(tabulate(list_of_records, headers=column_name, tablefmt="psql"))


class Command(BaseCommand):
    help="An interactive script where user can search for article title"

    def handle(self, *args, **options):
        if CoronaArticles.objects.exists():
            cosine_results_case_sensitive = {}
            cosine_results_case_insensitive = {}
            cosine_results_case_insensitive_without_special = {}
            jaccard_results_case_sensitive = {}
            jaccard_results_case_insensitive = {}
            jaccard_results_case_insensitive_without_special = {}

            str1 = input("Enter title to search: ")
            for object in CoronaArticles.objects.all():
                str2 = object.title

                # Computing Cosine Similarity for different cases
                # In this case we compare two strings case sensitive
                if get_cosine_similarity(str1, str2) != 0.0:
                    cosine_results_case_sensitive[object.id] = get_cosine_similarity(str1, str2)
                # In this case we compare two strings case insensitive
                low_str1 = str1.lower()
                low_str2 = str2.lower()
                if get_cosine_similarity(low_str1, low_str2) != 0.0:
                    cosine_results_case_insensitive[object.id] = get_cosine_similarity(low_str1, low_str2)
                # Comparing two case-insensitive strings by removing all the punctuations and special characters
                reg_str1 = re.sub('\W+', ' ', low_str1)
                reg_str2 = re.sub('\W+', ' ', low_str2)
                if get_cosine_similarity(reg_str1, reg_str2) != 0.0:
                    cosine_results_case_insensitive_without_special[object.id] = get_cosine_similarity(reg_str1, reg_str2)

                # Computing Jaccard Similarity for different cases
                # In this case we compare two strings case sensitive
                if get_jaccard_similarity(str1, str2) != 0.0:
                    jaccard_results_case_sensitive[object.id] = get_jaccard_similarity(str1, str2)
                # In this case we compare two strings case insensitive
                if get_jaccard_similarity(low_str1, low_str2) != 0.0:
                    jaccard_results_case_insensitive[object.id] = get_jaccard_similarity(low_str1, low_str2)
                # Comparing two case-insensitive strings by removing all the punctuations and special characters
                if get_jaccard_similarity(reg_str1, reg_str2) != 0.0:
                    jaccard_results_case_insensitive_without_special[object.id] = get_jaccard_similarity(reg_str1, reg_str2)

            # Reverse Sorting the results:
            # i) Cosine Similarity
            sorted_cosine_results_case_sensitive = dict(OrderedDict(
                sorted(cosine_results_case_sensitive.items(), key=lambda x: x[1], reverse=True)
            ))
            sorted_cosine_results_case_insensitive = dict(OrderedDict(
                sorted(cosine_results_case_insensitive.items(), key=lambda x: x[1], reverse=True)
            ))
            sorted_cosine_results_case_insensitive_without_special = dict(OrderedDict(
                sorted(cosine_results_case_insensitive_without_special.items(), key=lambda x: x[1], reverse=True)
            ))
            # print(f"Cosine Similarity case-sensitive results: {sorted_cosine_results_case_sensitive}")
            # print(f"Cosine Similarity case-insensitive results: {sorted_cosine_results_case_insensitive}")
            # print(f"Cosine Similarity case-insensitive results without punctuations and special characters: "
            #       f"{sorted_cosine_results_case_insensitive_without_special}")
            if len(sorted_cosine_results_case_sensitive):
                print("\nCosine Similarity case-sensitive results: \n")
                iterate_dictionary(sorted_cosine_results_case_sensitive)
            if len(sorted_cosine_results_case_insensitive):
                print("\nCosine Similarity case-insensitive results: \n")
                iterate_dictionary(sorted_cosine_results_case_insensitive)
            if len(sorted_cosine_results_case_insensitive_without_special):
                print("\nCosine Similarity case-insensitive results without punctuations and special characters: \n")
                iterate_dictionary(sorted_cosine_results_case_insensitive_without_special)


            # ii) Jaccard Similarity
            sorted_jaccard_results_case_sensitive = dict(OrderedDict(
                sorted(jaccard_results_case_sensitive.items(), key=lambda x: x[1], reverse=True)
            ))
            sorted_jaccard_results_case_insensitive = dict(OrderedDict(
                sorted(jaccard_results_case_insensitive.items(), key=lambda x: x[1], reverse=True)
            ))
            sorted_jaccard_results_case_insensitive_without_special = dict(OrderedDict(
                sorted(jaccard_results_case_insensitive_without_special.items(), key=lambda x: x[1], reverse=True)
            ))
            # print(f"Jaccard Similarity case-sensitive results: {sorted_jaccard_results_case_sensitive}")
            # print(f"Jaccard Similarity case-insensitive results: {sorted_jaccard_results_case_insensitive}")
            # print(f"Jaccard Similarity case-insensitive results without punctuations and special characters: "
            #       f"{sorted_jaccard_results_case_insensitive_without_special}")
            if len(sorted_jaccard_results_case_sensitive):
                print("\nJaccard Similarity case-sensitive results: \n")
                iterate_dictionary(sorted_jaccard_results_case_sensitive)
            if len(sorted_jaccard_results_case_insensitive):
                print("\nJaccard Similarity case-insensitive results: \n")
                iterate_dictionary(sorted_jaccard_results_case_insensitive)
            if len(sorted_jaccard_results_case_insensitive_without_special):
                print("\nJaccard Similarity case-insensitive results without punctuations and special characters: \n")
                iterate_dictionary(sorted_jaccard_results_case_insensitive_without_special)
        else:
            print("There is not data")

# Jaccard Similarity takes only unique set of words for each sentence/document while cosine similarity takes
# total length of the vectors. Ex: If you repeat the word "hello" in first string, cosine similarity changes,
# but jaccard similarity does not
# Jaccard similarity is good for cases where duplication does not matter,
# cosine similarity is good for cases where duplication matters while analyzing text similarity.
# Common use case:
# i)  Plagiarism: the cosine similarity would be ideal for plagiarism but jaccard similarity
#    would not be appropriate
# ii) Mirror Sites: the jaccard similarity would be ideal for determining mirror sites instead of cosine similarity
