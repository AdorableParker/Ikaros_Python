import jieba.analyse as ayse
import jieba.posseg as pseg

def Keyword_extraction(sentence, topK=3):
    keywords = ayse.extract_tags(sentence, topK=topK)
    if not keywords:
        keywords = sentence
    return keywords



def Chinese_compare(statement, other_statement):
    """
    Return the calculated similarity of two
    statements based on the Jaccard index.
    """

    pos_a = pseg.cut(statement)
    pos_b = pseg.cut(other_statement)

    lemma_a = [
        (token, pos) for token, pos in pos_a
    ]

    lemma_b = [
        (token, pos) for token, pos in pos_b
    ]

    # Calculate Jaccard similarity
    numerator = len(set(lemma_a).intersection(lemma_b))
    denominator = float(len(set(lemma_a).union(lemma_b)))
    ratio = numerator / denominator
    return ratio