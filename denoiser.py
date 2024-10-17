import numpy as np
from itertools import combinations
from collections import defaultdict

# --0. functions for maximum entropy randomization
def get_P(M:np.ndarray, a_in:dict, a_out:dict):
    P = np.zeros_like(M)
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            P[i,j] = 1 / (a_out[i] * a_in[j] + 1)
    return P


def randomize_matrix(M:np.ndarray, iters:int=100, saveHistory:bool=False, probHistory:bool=False):
    """randomize_matrix Randomize the directed weighted network with maximum entropy method

    Parameters
    ----------
    M : np.ndarray
        The directed weighted network in the form of adjacency matrix
    iters : int, optional
        The number of iterations, by default 100
    saveHistory : bool, optional
        Whether to save the history of alphas, by default False
    probHistory : bool, optional
        Whether to save the history of probabilities, by default False

    Returns
    -------
    P, a_in_his, a_out_his, probs_his
    """
    edges_dict = {}
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            edges_dict[(i,j)] = M[i,j]
    G = edges_dict
    G_nodes = set([i for i,j in G.keys()]+[j for i,j in G.keys()])

    # G0 is the complete graph with all the nodes
    G0 = set(combinations(G_nodes,2))
    G0 = G0 | set([(j,i) for i,j in G0]) | set([(i,i) for i in G_nodes])

    # adj list
    adj_out = defaultdict(list)
    adj_in = defaultdict(list)
    adj_in_weight = defaultdict(list)
    adj_out_weight = defaultdict(list)
    for e in G:
        adj_out[e[0]].append(e[1])
        adj_in[e[1]].append(e[0])
        adj_in_weight[e[1]].append(G[e])
        adj_out_weight[e[0]].append(G[e])
    adj0_out = defaultdict(list)
    adj0_in = defaultdict(list)
    for e in G0:
        adj0_out[e[0]].append(e[1])
        adj0_in[e[1]].append(e[0])
        
    a_in = dict.fromkeys(adj_in.keys(), 1)
    a_out = dict.fromkeys(adj_out.keys(), 1)

    # save the history of alphas
    a_in_his = [[] for _ in range(iters+1)]
    a_in_his[0] = list(a_in.values())
    a_out_his = [[] for _ in range(iters+1)]
    a_out_his[0] = list(a_out.values())
    probs_his = [[] for _ in range(iters)]
    # edges in the original graph that will be calculated the prob
    es = [e for e in G0 if e[0] in a_out and e[1] in a_in]

    sum_in = {}
    sum_out = {}
    for iter in range(iters):
        # 1. update a_in
        for i in adj_in.keys():
            sum_in[i] = 0
            for j in adj0_in[i]:
                if j in a_out:
                    sum_in[i] += 1 / (a_out[j] + 1 / a_in[i])
        # now the sum has been stored for each node with in-degree
        # update the a_in at the end of the iteration
        #a_in = {i: sum_in[i] / len(adj_in[i]) for i in adj_in.keys()}
        a_in = {i:sum_in[i]/ np.sum(adj_in_weight[i]) for i in adj_in.keys()}
        # 2. update a_out
        for i in adj_out.keys():
            sum_out[i] = 0
            for j in adj0_out[i]:
                if j in a_in:
                    sum_out[i] += 1 / (a_in[j] + 1 / a_out[i])
        # now the sum has been stored for each node with out-degree
        # update the a_out at the end of the iteration
        #a_out = {i: sum_out[i] / len(adj_out[i]) for i in adj_out.keys()}
        a_out = {i:sum_out[i]/ np.sum(adj_out_weight[i]) for i in adj_out.keys()}
        
        # save the history of alphas
        if saveHistory:
            a_in_his[iter+1] = list(a_in.values())
            a_out_his[iter+1] = list(a_out.values())

        if probHistory:
            probs = []
            for e in es:
                i, j = e
                probs.append(1 / (a_out[i] * a_in[j] + 1))
            probs_his[iter] = probs
            
    if saveHistory:
        a_in_his = np.array(a_in_his)
        a_out_his = np.array(a_out_his)
    if probHistory:
        probs_his = np.array(probs_his)
    
    P = get_P(M, a_in, a_out)
    
    return P, a_in_his, a_out_his, probs_his

def calculate_uncertainty(a,b,a_std,b_std):
    e = np.exp(1)
    M, N = len(a), len(b)
    sigma_P = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            partial_a =  - (e**(-(a[i]+b[j]))) / (1 + e**(-(a[i]+b[j]))) ** 2
            partial_b = - (e**(-(a[i]+b[j]))) / (1 + e**(-(a[i]+b[j]))) ** 2
            sigma_P[i, j] = (partial_a ** 2) * (a_std[i] ** 2) + (partial_b ** 2) * (b_std[j] ** 2)
    return np.sqrt(sigma_P)