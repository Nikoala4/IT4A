import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import time
import random
import sys
import math

sys.setrecursionlimit(10000)

def bubble_sort(A):
    n = len(A)

    flag = 1
    for i in range(n-1):
        flag = 0
        for j in range(n-1-i):
            if A[j]>A[j+1]:            
                t = A[j]
                A[j]=A[j+1]
                A[j+1] = t
                flag = 1

        if flag == 0:
            break
    return A

def bubble_sort_optimized(A):
    n = len(A)
    while n > 1:
        newn = 0
        for i in range(1, n):
            if A[i-1] > A[i]:
                # Échange des éléments
                A[i-1], A[i] = A[i], A[i-1]
                # Mise à jour de la position du dernier échange
                newn = i
        # Réduction de la portée du tri à la dernière position échangée
        n = newn
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

def heapify(A, n, i):
    largest = i  # On suppose que l'élément courant est le plus grand
    left = 2 * i + 1  # Fils gauche
    right = 2 * i + 2  # Fils droit

    if left < n and A[left] > A[largest]:  # Si le fils gauche est plus grand
        largest = left

    if right < n and A[right] > A[largest]:  # Si le fils droit est plus grand
        largest = right

    if largest != i:  # Si l'un des fils est plus grand, on échange et on continue la réorganisation
        A[i], A[largest] = A[largest], A[i]
        heapify(A, n, largest)  # Appel récursif pour assurer la validité du tas

def heap_sort(A):
    n = len(A)
    # On construit un tas max
    for i in range(n // 2 - 1, -1, -1):
        heapify(A, n, i)

    # On extrait les éléments un par un
    for i in range(n - 1, 0, -1):
        A[i], A[0] = A[0], A[i]  # On place l'élément max en fin de tableau
        heapify(A, i, 0)  # On réorganise le tas
    return A


def partition(A, start, end, cpt_comp, cpt_swap):
    pivot = A[end]
    i = start - 1

    for j in range(start, end):
        cpt_comp += 1  # comparaison entre A[j] et pivot
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
            cpt_swap += 1  # permutation

    A[i + 1], A[end] = A[end], A[i + 1]
    cpt_swap += 1  # permutation

    return i + 1, cpt_comp, cpt_swap

def quick_sort_with_stats(A, start, end, cpt_comp=0, cpt_swap=0):
    if start < end:
        pivot_index, cpt_comp, cpt_swap = partition(A, start, end, cpt_comp, cpt_swap)
        cpt_comp, cpt_swap = quick_sort_with_stats(A, start, pivot_index - 1, cpt_comp, cpt_swap)
        cpt_comp, cpt_swap = quick_sort_with_stats(A, pivot_index + 1, end, cpt_comp, cpt_swap)

    return cpt_comp, cpt_swap

def quick_sort_main_with_stats(A):
    cpt_comp, cpt_swap = quick_sort_with_stats(A, 0, len(A) - 1)
    return A, cpt_comp, cpt_swap

def partition_default(A, start, end):
    pivot = A[end]  # Le dernier élément est choisi comme pivot
    iPivot = start  # L'indice du premier élément plus petit ou égal au pivot
    for i in range(start, end):  # On parcourt la partie du tableau à partitionner
        if A[i] <= pivot:  # Si l'élément est plus petit ou égal au pivot
            A[i], A[iPivot] = A[iPivot], A[i]  # On le place avant le pivot
            iPivot += 1  # On avance l'indice de la position pivot
    A[iPivot], A[end] = A[end], A[iPivot]  # On place le pivot à sa position finale
    return iPivot

def quick_sort(A, start=0, end=None):
    if end is None:
        end = len(A) - 1  # Initialisation de la borne supérieure
    if start < end:  # Si la sous-partie à trier contient au moins 2 éléments
        iPivot = partition_default(A, start, end)  # Partitionnement autour du pivot
        quick_sort(A, start, iPivot - 1)  # Tri récursif de la première partie
        quick_sort(A, iPivot + 1, end)  # Tri récursif de la deuxième partie
    return A