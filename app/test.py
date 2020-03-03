import numpy as np
from numpy.linalg import norm

vector_a = np.array([0, 0, 0, 0, 0, 0.1])

dataframe = np.array([[0.2,0,1,0,0.5,0.7], [0,0.5,1,0,0.5,0.7], [0,0,1,0.8,0.5,0.7], [0,0.10,1,0,0.5,0.7], [0,0,0,0,0,0]] ).T

cos_sim = np.dot(vector_a, dataframe)/(norm(vector_a)*norm(dataframe))

print(cos_sim)