
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import time

def insertion_sort(A):
    n = len(A)
    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key
    return A
def selection_sort(A):
    n = len(A)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if A[j] < A[min_idx]:
                min_idx = j
        if min_idx != i:
            t = A[i]
            A[i] = A[min_idx]
            A[min_idx] = t
    return A

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

def calculer_cas_moyen_tri_insertion(fct_tri, type_donnees='random', nlist=15, nval=200):
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

    plt.plot(taille_tableaux, operations_par_taille, label='Tri par insertion',linestyle=':', marker='+')
    plt.xlabel('Taille du tableau')
    plt.title('Nombre de permutations par taille de tableau')

    plt.legend()

    plt.grid(True, linestyle='--')

    plt.title('Nombre de permutations par taille de tableau')
    plt.legend()
    plt.grid(True)
    plt.show()

    return operations_par_taille

# fonction mettant en concurrence une liste de fonctions de tri, pour un type de données (tableau random, trié, inversé, partiellement trié, avec doublons)
def executerTriConcurrence(liste_fct_tri, liste_noms, liste_couleurs=['r', 'y', 'g', 'b', 'm','c'], nlist=15, nval=200, surplace=True, liste=['random', 'sorted', 'inverted', 'partial', 'duplicates']):
    axis, listDataRandom, listDataSorted, listDataInvertedSorted, listDataPartiallySorted, listDataWithDuplicates = create_data(nlist, nval)

    # Stockage des résultats pour les nouveaux cas
    toplot = {case: [[] for _ in range(len(liste_fct_tri))] for case in liste}

    # Duplication des données pour préserver les listes originales
    dataTest = {
        'random': [copy.deepcopy(listDataRandom) for _ in range(len(liste_fct_tri))],
        'sorted': [copy.deepcopy(listDataSorted) for _ in range(len(liste_fct_tri))],
        'inverted': [copy.deepcopy(listDataInvertedSorted) for _ in range(len(liste_fct_tri))],
        'partial': [copy.deepcopy(listDataPartiallySorted) for _ in range(len(liste_fct_tri))],
        'duplicates': [copy.deepcopy(listDataWithDuplicates) for _ in range(len(liste_fct_tri))]
    }
    liste_symboles = {'random':'-', 'sorted':'--','inverted':':','partial': '-.','duplicates': '-'}

    # Boucle sur les tailles d'axes
    for i in range(len(axis)):
        # Mesure des temps pour chaque cas
        for case in liste:
            for j in range(len(liste_fct_tri)):
                time1 = time.time()
                if surplace:
                    liste_fct_tri[j](dataTest[case][j][i])
                else:
                    dataTest[case][j][i] = liste_fct_tri[j](dataTest[case][j][i])
                time2 = time.time()
                toplot[case][j].append(time2 - time1)

    # Tracé des résultats pour chaque type de données
    for case in liste:
        for i in range(len(liste_fct_tri)):
            plt.plot(axis, toplot[case][i], liste_symboles[case] + liste_couleurs[i], label=liste_noms[i] + ' (' + case + ')')
    plt.legend()
    plt.show()
