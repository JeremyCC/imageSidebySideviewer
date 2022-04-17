'''
COPYRIGHT © 2020 JeremyCC, Github

Distribution is allowed under License
"GNU General Public License v3.0"

'''


import matplotlib.pyplot as plt
import imageSidebySideviewer


if __name__=='__main__':
    print(imageSidebySideviewer.__version__)
    imagenow = plt.imread('Example\\pic1.png')
    imagenow2 = plt.imread('Example\\pic2.png')

    imageSidebySideviewer.compare([imagenow,imagenow2],name=['Fig1','Fig2'],contrastminmax=[[0,125]],mode=0,colormapping=None,showhelp=True)

    '''
    mode 0: show all images separately
    mode 1: show all the images on a single window, will be slower under this mode
    '''
