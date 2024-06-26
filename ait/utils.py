import numpy as np
import pandas as pd
from PIL import Image
from skimage.measure import label


def get_r(input_array):
    '''
    Get the r values for input array with given dimensions.
    Return a cube with r in each cell
    '''
    dim = len(input_array.shape)
    if dim == 1:
        return get_r_1d(input_array)
    elif dim == 2:
        return get_r_2d(input_array)
    elif dim == 3:
        return get_r_3d(input_array)


def get_r_1d(input_array):
    x = np.arange(len(input_array))
    center = x.max() / 2.
    rx = (x - center)
    return [rx], rx


def get_r_2d(input_array):
    x, y = np.indices(input_array.shape)
    center = np.array([(x.max() - x.min()) / 2, (y.max() - y.min()) / 2])
    rx = (x - center[0])
    ry = (y - center[1])
    r = np.sqrt(rx**2 + ry**2)
    return [rx, ry], r


def get_r_3d(input_array):
    nx, ny, nz = input_array.shape
    x, y, z = np.indices(input_array.shape)
    center = np.array([nx/2 if nx%2==0 else (nx-1)/2, ny/2 if ny%2==0 else (ny-1)/2, \
                        nz/2 if nz%2==0 else (nz-1)/2])
    rx = (x - center[0])
    ry = (y - center[1])
    rz = (z - center[2])

    r = np.sqrt(rx**2 + ry**2 + rz**2)
    return [rx, ry, rz], r


def read_png(path):
    img = Image.open(path)
    img = np.array(img)
    return img


def save_png(img, path):
    # img should be [0, 255]
    img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    img.save(path)


# TODO: test
def get_isolate(arr, lower_cut=0, larger_cut=np.inf, **kwargs):
    '''
    Get the isolated region of an array,
    where the size of the region is larger than lower_cut
    and smaller than larger_cut.
    '''
    clusters = label(arr, **kwargs)
    cluster_sizes = np.bincount(clusters.ravel())
    good_clusters = np.where((cluster_sizes > lower_cut)
                             & (cluster_sizes < larger_cut))[0]
    return np.isin(clusters, good_clusters)


def get_unique_name(names, name_lst, name_pattern='{name}_{i}'):

    # if name is not list
    if not isinstance(names, list):
        names = [names]
        is_single_name = True
    else:
        is_single_name = False

    k = len(names)

    i = 0
    while any(name in name_lst for name in names):

        for j in range(k):
            names[j] = name_pattern.format(name=names[j], i=i)
        i += 1

    if is_single_name:
        names = names[0]

    return names


def is_string_series(s: pd.Series):
    # https://stackoverflow.com/questions/43049545/python-check-if-dataframe-column-contain-string-type
    if isinstance(s.dtype, pd.StringDtype):
        # The series was explicitly created as a string series (Pandas>=1.0.0)
        return True
    elif s.dtype == 'object':
        # Object series, check each value
        return all((v is None) or isinstance(v, str) for v in s)
    else:
        return False
