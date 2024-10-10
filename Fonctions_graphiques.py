
import matplotlib.pyplot as plt
import numpy as np
import random

def create_data(nlist=15, nval=200):
    # Création de listes de taille incrémentale et de contenu varié
    listDataRandom = []
    listDataSorted = []
    listDataInversedSorted = []
    listDataPartiallySorted = []
    listDataWithDuplicates = []
    sizeArrays = []

    # Remplissage des listes
    for i in range(1, nlist + 1):
        s = nval * i
        dataRandom = list(range(s))
        dataSorted = list(range(s))
        dataInversed = list(range(s))
        dataPartiallySorted = list(range(s))
        dataWithDuplicates = [random.randint(0,s-1) for _ in range(s)]  # Listes avec doublons

        # Appliquer les transformations
        dataInversed.reverse()
        random.shuffle(dataRandom)
        random.shuffle(dataPartiallySorted)

        # Rendre une partie du tableau partiellement triée
        part = s // 2
        dataPartiallySorted[part:] = sorted(dataPartiallySorted[part:])

        # Ajouter les listes à leurs ensembles respectifs
        listDataRandom.append(dataRandom)
        listDataSorted.append(dataSorted)
        listDataInversedSorted.append(dataInversed)
        listDataPartiallySorted.append(dataPartiallySorted)
        listDataWithDuplicates.append(dataWithDuplicates)
        sizeArrays.append(s)

    return (sizeArrays, listDataRandom, listDataSorted, listDataInversedSorted, listDataPartiallySorted, listDataWithDuplicates)

def calculer_cas_moyen_tri_bulles(fct_tri, type_donnees='random', nlist=15, nval=200):
    operations = []
    tailles = []

    operations_par_taille = [0] * nlist

    # Création des tableaux
    taille_tableaux, listDataRandom, listDataSorted, listDataInvertedSorted, listDataPartiallySorted, listDataWithDuplicates = create_data(nlist, nval)
    dataTest = {
        'random': listDataRandom,
        'sorted': listDataSorted,
        'inverted': listDataInvertedSorted,
        'partial': listDataPartiallySorted,
        'duplicates': listDataWithDuplicates
    }

    for i, data in enumerate(dataTest[type_donnees]):
        _,_, ops = fct_tri(data)
        operations_par_taille[i] += ops

    operations_par_taille = [ops for ops in operations_par_taille]
    # Courbe théorique n^2/4
    operations_theoriques = [(n**2)/4 for n in taille_tableaux]
    plt.plot(taille_tableaux, operations_theoriques, label='n^2/4', linestyle='--')

    plt.plot(taille_tableaux, operations_par_taille, label='Tri à bulles',linestyle=':', marker='+')
    plt.xlabel('Taille du tableau')
    plt.title('Nombre de permutations par taille de tableau')

    plt.legend()

    plt.grid(True, linestyle='--')

    plt.title('Nombre de permutations par taille de tableau')
    plt.legend()
    plt.grid(True)
    plt.show()

    return operations_par_taille
