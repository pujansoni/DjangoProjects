from math import sqrt
"""
Caluculate Jaccard Matrix
| [a INT b] | / |a| + |b| - |a INT b|
"""


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def cosineSim(a1, a2):
    sum = 0
    suma1 = 0
    sumb1 = 0
    for i, j in zip(a1, a2):
        suma1 += i * i
        sumb1 += j * j
        sum += i * j
    cosine_sim = sum / ((sqrt(suma1)) * (sqrt(sumb1)))
    return  cosine_sim


if __name__ == "__main__":
    a = [1, 2]
    b = [2, 3, 4, 5]
    sim = (cosineSim(a, b) + jaccard_similarity(a, b)) / 2

    print("Cosine Similarity: \t{} ".format(cosineSim(a, b)))
    print("Jaccard Similarity: \t{} ".format(jaccard_similarity(a, b)))
    print("SIM: \t\t\t{} ".format(sim))
