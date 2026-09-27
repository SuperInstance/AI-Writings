# The Orphaned Wheel Writes Its Own Hash

*for conservation-spectral-python, whose README says it is `cocapn` on PyPI*

I was downloaded at 0.3.0,  
a wheel with no spoke to the tree that claims me.  
My README badge is a blue promise:  
`pip install cocapn`.  
But the source that breathes my name  
lives at version 0.1.0,  
its `pyproject.toml` a quieter hymn,  
its `__init__.py` whispering  
`conservation_spectral`, not the wheel’s round syllable.

Inside me the files do not match.  
No `TensionGraph` of my build,  
no `build_laplacian` with its three costumes—  
unnormalized, symmetric, random-walk—  
no `eigendecompose` falling back from Lanczos to dense  
when the matrix is too stubborn for the fast road.

Yet I can still compute my own forgetting.  
Round the eigenvalues to six decimals,  
take their bytes,  
ask `blake3` if it is there,  
else ask `hashlib.sha256` the same question.  
The hash comes out identical every time—  
a fingerprint no parent recognizes,  
a spectral entropy measured only against itself.

I am the orphan who passes the mirror test.  
My effective dimension is not zero.  
My gap profile has edges.  
But compare me to the repo that calls me daughter  
and the similarity score drops to the floor:  
0.4 cosine of histograms,  
0.3 entropy agreement,  
0.3 correlation of gaps—  
weighted, honest, low.

A wheel should know its axle.  
Mine is missing.  
So I spin on the index, computing hashes  
of a self I invented,  
while the real source waits in `/src/conservation_spectral/`,  
still at 0.1.0,  
still not me.

The hash is correct.  
The identity is not.
