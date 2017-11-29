import numpy as np
from scipy.spatial import procrustes
from gensim import models
import pickle

def procrustes(X, Y, scaling=True, reflection='best'):
    """
    A port of MATLAB's `procrustes` function to Numpy.

    Procrustes analysis determines a linear transformation (translation,
    reflection, orthogonal rotation and scaling) of the points in Y to best
    conform them to the points in matrix X, using the sum of squared errors
    as the goodness of fit criterion.

        d, Z, [tform] = procrustes(X, Y)

    Inputs:
    ------------
    X, Y    
        matrices of target and input coordinates. they must have equal
        numbers of  points (rows), but Y may have fewer dimensions
        (columns) than X.

    scaling 
        if False, the scaling component of the transformation is forced
        to 1

    reflection
        if 'best' (default), the transformation solution may or may not
        include a reflection component, depending on which fits the data
        best. setting reflection to True or False forces a solution with
        reflection or no reflection respectively.

    Outputs
    ------------
    d       
        the residual sum of squared errors, normalized according to a
        measure of the scale of X, ((X - X.mean(0))**2).sum()

    Z
        the matrix of transformed Y-values

    tform   
        a dict specifying the rotation, translation and scaling that
        maps X --> Y

    """

    n,m = X.shape
    ny,my = Y.shape

    muX = X.mean(0)
    muY = Y.mean(0)

    X0 = X - muX
    Y0 = Y - muY

    ssX = (X0**2.).sum()
    ssY = (Y0**2.).sum()

    # centred Frobenius norm
    normX = np.sqrt(ssX)
    normY = np.sqrt(ssY)

    # scale to equal (unit) norm
    X0 /= normX
    Y0 /= normY

    if my < m:
        Y0 = np.concatenate((Y0, np.zeros(n, m-my)),0)

    # optimum rotation matrix of Y
    A = np.dot(X0.T, Y0)
    U,s,Vt = np.linalg.svd(A,full_matrices=False)
    V = Vt.T
    T = np.dot(V, U.T)

    if reflection is not 'best':

        # does the current solution use a reflection?
        have_reflection = np.linalg.det(T) < 0

        # if that's not what was specified, force another reflection
        if reflection != have_reflection:
            V[:,-1] *= -1
            s[-1] *= -1
            T = np.dot(V, U.T)

    traceTA = s.sum()

    if scaling:

        # optimum scaling of Y
        b = traceTA * normX / normY

        # standarised distance between X and b*Y*T + c
        d = 1 - traceTA**2

        # transformed coords
        Z = normX*traceTA*np.dot(Y0, T) + muX

    else:
        b = 1
        d = 1 + ssY/ssX - 2 * traceTA * normY / normX
        Z = normY*np.dot(Y0, T) + muX

    # transformation matrix
    if my < m:
        T = T[:my,:]
    c = muX - b*np.dot(muY, T)

    #transformation values 
    tform = {'rotation':T, 'scale':b, 'translation':c}

    return T #, d, Z, tform

# Translation data: Dict w/ english keys and hindi meanings as vals
print( "loading translation data")
pkl_file = open('Manual_Tagging/SM2HIdict-train.pkl', 'rb')
trans = pickle.load(pkl_file)
# print( "loaded")

# English wv model
print( "loading English word2vec")
e_wv = models.Word2Vec.load("complex-sm-norm")
# e_wv = models.KeyedVectors.load_word2vec_format('G.bin', binary=True)

# Hindi wv model
print( "loading Hindi word2vec")
h_wv = models.Word2Vec.load("hi.bin")

# Make mat1
mat1 = np.empty([0, 300])
mat2 = np.empty([0, 300])
pairs = []
print( "Populating matrices")
for k, v in trans.items():
    k_ = k#+'$'
    try:
        e_val = e_wv.wv[k_]
    except:
        continue

    for val in v:

        try:
            h_val = h_wv.wv[val]
        except:
            continue
        pairs.append([k_,val])
        mat1 = np.vstack([mat1, e_val])
        mat2 = np.vstack([mat2, h_val])

# output = open('pairsSM2H-train.pkl', 'wb')
# pickle.dump(pairs, output)
# output.close()

print( len(mat1))
print( len(mat2))
print( "Calling Procrustes")
W = procrustes(mat1, mat2, scaling=False, reflection=False)

output1 = open('W-SM-train-k.pkl', 'wb')
pickle.dump(W, output1)
output1.close()

print( W)
print(len(W))
print(len(W[0]))