def jaccard_ngramas(word1, word2, n=2):
    # Crear los n-gramas para ambas palabras
    ngrams1 = set([word1[i:i+n] for i in range(len(word1)-n+1)])
    ngrams2 = set([word2[i:i+n] for i in range(len(word2)-n+1)])
    
    # Calcular la intersección y la unión de los conjuntos de n-gramas
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    
    # Devolver la similitud de Jaccard
    return intersection / union

def similitud_j(word_list, target_word, n=2):
    # Calcular la similitud para cada palabra en la lista
    similarities = [jaccard_ngramas(word, target_word, n) for word in word_list]
    
    # Encontrar el índice de la palabra con la mayor similitud
    max_similarity_index = similarities.index(max(similarities))
    return max_similarity_index

# Ejemplo de uso
palabras = ["gato12iu", "gatogato", "gato pequeño", "gato", "gatos", "gatubela", "gato1", "gato1", "gato1", "gato1", "gato ato"]
palabra_comparar = "gato peq"
indice = similitud_j(palabras, palabra_comparar)

print(f"La palabra más parecida a '{palabra_comparar}' es: {palabras[indice]}")
