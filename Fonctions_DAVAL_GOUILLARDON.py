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


def calculer_cas_moyen_avec_stats(fct_tri, type_donnees='random', nlist=15, nval=200):
    comparaisons_par_taille = []
    permutations_par_taille = []
    tailles = []

    # Création des tableaux
    taille_tableaux, listDataRandom, listDataSorted, listDataInvertedSorted, _, _ = create_data(nlist, nval)
    
    dataTest = {
        'random': listDataRandom,
        'sorted': listDataSorted,
        'inverted': listDataInvertedSorted
    }

    # Sélection des données à tester en fonction du type_donnees
    data_test = dataTest[type_donnees]
    
    # Parcours des différentes tailles de tableaux pour effectuer les tris
    for i, data in enumerate(data_test):
        _, nb_comparaisons, nb_permutations = fct_tri(data)
        
        # Ajout des résultats dans les listes correspondantes
        comparaisons_par_taille.append(nb_comparaisons)
        permutations_par_taille.append(nb_permutations)
        tailles.append(len(data))

    # Courbe théorique n^2/4 pour comparaison (comparaisons et permutations attendues pour certains tris quadratiques)
    operations_theoriques = [n*math.log(n) for n in tailles]

    # Tracé des résultats (comparaisons)
    plt.plot(tailles, operations_theoriques, label='n log(n) Comparaisons théoriques', linestyle='--')
    plt.plot(tailles, comparaisons_par_taille, label=f'{fct_tri.__name__} - Comparaisons', linestyle=':', marker='+')

    # Tracé des résultats (permutations)
    plt.plot(tailles, permutations_par_taille, label=f'{fct_tri.__name__} - Permutations', linestyle=':', marker='o')

    plt.xlabel('Taille du tableau')
    plt.ylabel('Nombre d\'opérations')
    plt.title(f'Comparaisons et Permutations ({fct_tri.__name__}) par taille de tableau')

    plt.legend()
    plt.grid(True, linestyle='--')
    plt.show()

    return comparaisons_par_taille, permutations_par_taille


def executerTri(fct_tri, color, nom, nlist=15, nval=200, surplace=True):
    axis, listDataRandom, listDataSorted, listDataInvertedSorted, listDataPartiallySorted, listDataWithDuplicates = create_data(nlist, nval)

    # Stockage des résultats pour les nouveaux cas
    toplotRandom = []
    toplotSorted = []
    toplotInverted = []
    toplotPartial = []
    toplotDuplicates = []

    # Duplication des données pour préserver les listes originales
    dataTestRandom = copy.deepcopy(listDataRandom)
    dataTestSorted = copy.deepcopy(listDataSorted)
    dataTestInverted = copy.deepcopy(listDataInvertedSorted)
    dataTestPartial = copy.deepcopy(listDataPartiallySorted)
    dataTestDuplicates = copy.deepcopy(listDataWithDuplicates)

    # Boucle sur les tailles d'axes
    for i in range(len(axis)):
        # Mesure des temps pour chaque cas
        for dataType, toplot, dataTest in [
            (dataTestRandom, toplotRandom, dataTestRandom),
            (dataTestSorted, toplotSorted, dataTestSorted),
            (dataTestInverted, toplotInverted, dataTestInverted),
            (dataTestPartial, toplotPartial, dataTestPartial),
            (dataTestDuplicates, toplotDuplicates, dataTestDuplicates)
        ]:
            time1 = time.time()
            if surplace:
                fct_tri(dataTest[i])
            else:
                dataTest[i] = fct_tri(dataTest[i])
            time2 = time.time()
            toplot.append(time2 - time1)

    # Tracé des résultats pour chaque type de données
    plt.plot(axis, toplotRandom, '-' + color, label=nom + ' (random)')
    plt.plot(axis, toplotSorted, '--' + 'b', label=nom + ' (sorted)')
    plt.plot(axis, toplotInverted, ':' + 'g', label=nom + ' (inverted)')
    plt.plot(axis, toplotPartial, '-.' + 'y', label=nom + ' (partial)')
    plt.plot(axis, toplotDuplicates, ':' + color, label=nom + ' (duplicates)')
    plt.legend()
    plt.show()

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

def merge(left, right, cpt_comp, cpt_swap):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        cpt_comp += 1  # comparaison entre left[i] et right[j]
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            cpt_swap += 1  # permutation
    result.extend(left[i:])
    result.extend(right[j:])
    return result, cpt_comp, cpt_swap

def merge_sort(A):
    if len(A) > 1:
        mid = len(A) // 2
        L = A[:mid]
        R = A[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                A[k] = L[i]
                i += 1
            else:
                A[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            A[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            A[k] = R[j]
            j += 1
            k += 1
    return A

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