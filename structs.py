# -*- coding: utf-8 -*-

import numpy as np


# Описание структуры данных определенной локации
LocalDS = np.dtype([
    ('time', np.float64),
    ('O3', np.float32, (140,)),
    ('O3Err',np.float32, (140,)),
    ('TH', np.float32),
    ('Ext386', np.float32, (80,)),
    ('Ext452', np.float32, (80,)),
    ('Ext525', np.float32, (80,)),
    ('Ext1020', np.float32, (80,)),
    ('Ext386_Err', np.float32, (80,)),
    ('Ext452_Err', np.float32, (80,)),
    ('Ext525_Err', np.float32, (80,)),
    ('Ext1020_Err', np.float32, (80,)),
])


