import numpy as np

# data1 = np.array([40, 30, 20, 10])
# data1 = np.array([40, 30.0, 20, 10])
# data1 = np.array([40, 30, 20, 10], dtype=float)
data1 = np.array([40, 30.0, "inha", 10])
print(data1)

data2 = np.array([[1, 2],[3, 4]])
print(data2)

data3 = np.zeros((3, 4, 2))
print(data3)

data4 = np.ones((8))
print(data4)
# arange, full, linspace ... np.random.rand()

print(data1.dtype, data2.dtype, data3.dtype, data4.dtype)
print(data1.ndim, data2.ndim, data3.ndim, data4.ndim)
print(data1.shape, data2.shape, data3.shape, data4.shape)
# size, T, itemsize ...



