import numpy as np
from utils.similarity import calc_dist
from homepage.models import Homepage

def get_student(emb):
    for i in Homepage.objects.all().values_list('Roll_NUmber','Name','Image_Vector','email'):
        p=list(i[2].split(','))
        p[0]=p[0][1:]
        p[-1]=p[-1][:-1]
        k=[float(i) for i in p]
        dist=calc_dist(k,emb)
        if dist<1:
            return i[0],i[1],i[3]
    return 'Not Found','Not Found','Not Found'
