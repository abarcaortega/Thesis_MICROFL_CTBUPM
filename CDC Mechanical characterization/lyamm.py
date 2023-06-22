import matplotlib.pyplot as plt
import numpy as np
import glob, os
from skimage.measure import profile_line
from scipy.optimize import curve_fit
from skimage import io
from scipy import signal
from matplotlib.backend_bases import FigureCanvasBase, MouseButton
#import scipy.io.wavfile
from simple_colors import *
from PIL import Image
import cv2
import argparse
import imutils


def nam (type):
    cwd = os.getcwd()

    if type == "dir":
        tp = "/exp_*/"
        l = -2
    if type == "txt":
        tp = "/*.txt"
        l = -1
    s = glob.glob(cwd+tp)
    names = list()

    for i in range(len(s)):
        names.append((s[i].split("\\"))[l])

    return names

def status():

    cwd = os.getcwd()

    nams = nam("dir")
    
    
    #print(nams)

    try:
        os.mkdir("Results")
    except:
        pass

    os.chdir("Results")
    r = nam("txt")
    rl = list()

    nams = ['res_' + s for s in nams]
    for i in range(len(r)):
        rl.append((r[i].split(".txt"))[0])

    tot = 0
    nlist = list()

    for i in range(len(nams)):

        if nams[i] != "Results":
            nlist.append(nams[i])

        if any(x == nams[i] for x in rl):
            nlist.remove(nams[i])
            tot += 1

    nxt = nlist[0]
    msg = "Analisys complete "+str(tot)+" of "+str(len(nams))+". Next analysis: "+nxt

    print(msg)
    os.chdir(cwd)

    return nxt,len(nlist)

def theret(x,e):
    return (3*2.1)/(2*np.pi)*(1/e)*x

def plaza(x,dia,Rp,e):
    b1 = np.single(2.0142)
    b3 = np.single(2.1187)
    R0 = dia/2
    return (1/(b1*(1-(Rp/R0)**b3)))*(3/e)*x

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def res_an(xdata, ydata, dia, Rp):
    #xdata = data[:][0]
    #ydata = data[:][1]
    x = []
    min_d = []
    max_d = []

    xpass = 0
    
    while xpass == 0:
        input(" Please, select the correct range for the results. Select two points and then close the plot. (Enter to continue)")
        try:
            plt.plot(xdata, ydata, 'b-', label='data')
            plt.ylabel('$L_p/R_p$')
            plt.xlabel('$\Delta P$')
            plt.legend()
            x = plt.ginput(n=2, timeout=0, show_clicks=True)
            xpass = 1
        except:
            x = [(0,0), (0,0)]
    
    min_d = np.where(xdata == float(find_nearest(xdata,x[0][0])))[0][0]
    max_d = np.where(xdata == float(find_nearest(xdata,x[1][0])))[0][0]
    
    plt.show()
    
    for i in range(len(xdata)-max_d):
        xdata = np.delete(xdata, -1)
        ydata = np.delete(ydata, -1)
    
    try:
        for i in range(min_d):
            xdata = np.delete(xdata, 0)
            ydata = np.delete(ydata, 0)
    except:
        pass
    
    her = []
    for i in range(len(ydata)-1):
        if abs(np.round(ydata[i],4)) == float(0):
            her = np.append(her, i)
    
    for item in reversed(her):
        xdata = np.delete(xdata, int(item))
        ydata = np.delete(ydata, int(item))
    #fig.canvas.mpl_connect('pick_event', onpick2)
    
    for i in range(len(xdata)-1):
        xdata[i+1] = xdata[i+1]-xdata[0]
        ydata[i+1] = ydata[i+1]-ydata[0]
    
    xdata[0] = 0
    ydata[0] = 0
    
    plt.plot(xdata, ydata, 'b-', label='Experimental data')
    plt.ylabel('$L_p/R_p$')
    plt.xlabel('$\Delta P$')
    plt.xlim(0, np.max(xdata)*1.1)
    plt.ylim(0, np.max(ydata)*1.1)
    plt.legend()
    popt, pcov = curve_fit(theret, xdata, ydata)
    the_e = popt
    
    plt.plot(xdata, theret(xdata, *popt), 'r-', label='Theret et al.: $E_{ap}$ = %5.3f' % tuple(popt))
    
    #popt, pcov = curve_fit(plaza, xdata, ydata, bounds=((float(dia)*0.9999999, float(Rp)*0.999999, 0), (float(dia), float(Rp), np.inf)))
    popt, pcov = curve_fit(lambda x, e: plaza(x,dia,Rp,e), xdata, ydata)
    plz_e = popt
    
    #print(*popt)
    plt.plot(xdata, plaza(xdata, dia, Rp, popt), 'g--', label='Plaza et al.: $E_{ap}$ = %5.3f' % popt)
    
    # plt.plot(xdata, func(xdata, *popt), 'g--', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    plt.ylabel('$L_p/R_p$')
    plt.xlabel('$\Delta P$')
    plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show()

    return xdata, ydata, the_e, plz_e

def press():
    cwd = os.getcwd()
    
    date = cwd[-10:]  # The experiments needs to be register as "Name_year_mo_dy"
    
    l2 = glob.glob("*RAMPA.jpeg")
    #print(l2)
    l1 = l2[0]
    l1 = l1[:16]
    h = np.zeros(len(l2))
    i = 0
    #print(l1)
    x = 0
    while x == 0:
        g = glob.glob("Register_experiments_" + date + "*")
        g1 = glob.glob("Data."+"txt")
        # print(len(g1))
        # print(len(g))
        if len(g) == 0 and len(g1) == 0:
            os.chdir("..")
        else:
            break
    k=0
    len(l2)
    
    try:
        with open(g[0]) as f:
            for line in f:
                linedata = line.split('\t')
                #print(linedata)
                #print(l2[k])
                #print((l2[k])[:(len(l2[k])-7)])
                if (l2[k])[:(len(l2)-7)] in str(linedata):
                    h[i] = abs(float(linedata[2])) * 9.81
                    i = i + 1
                    k = k+1
                    if k >= len(l2):
                        break
    except:
        with open(g1[0]) as f:
            for line in f:
                linedata = line.split('\t')
                #print(linedata)
                #print(l2[k])
                #print((l2[k])[:(len(l2[k])-7)])
                if (l2[k])[:(len(l2)-7)] in str(linedata):
                    h[i] = abs(float(linedata[2])) * 9.81
                    i = i + 1
                    k = k+1
                    if k >= len(l2):
                        break
    
    os.chdir(cwd)
    return h
    
def yes_or_no(question):
    hx = 1
    while hx == 1:
        answer = input(question + ' (y/n): ').lower().strip()
        if answer in ('y', 'yes', 'n', 'no'):
            if answer in ('y', 'yes'):
              hhhh = 1
              hx = 0
              return hhhh
            if answer in ('n', 'no'):
               hhhh = 0
               hx = 0
               return hhhh
            else:
               print('You must answer yes or no.')
               
def coord(name,scale):
    im = cv2.imread(name)
    large = cv2.resize(im, (0,0), fx=scale, fy=scale) 

    r = cv2.selectROI(large)
    rr = np.zeros(len(r))
    rr[0] = round(r[0]/scale)
    rr[1] = round(r[1]/scale)
    rr[2] = round(r[2]/scale)
    rr[3] = round(r[3]/scale)

    cv2.destroyAllWindows()
    return rr

def rotate_image(image, angle):
  
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  
  return result

def crop(name,rr,rotate,ang_ent):
    
    im = cv2.imread(name)
    imCrop = im[int(rr[1]):int(rr[1]+rr[3]), int(rr[0]):int(rr[0]+rr[2])]
    ang = 0
    dthet = 0
    ang_1 = np.zeros(2)
    hi = 0
    
    try:
                
        while rotate == 0:
            
            if hi == 0:
                imCrop = rotate_image(im[int(rr[1]):int(rr[1]+rr[3]), int(rr[0]):int(rr[0]+rr[2])],ang_1[1])
            if hi == 1:
                imCrop = rotate_image(im[int(rr[1]):int(rr[1]+rr[3]), int(rr[0]):int(rr[0]+rr[2])],ang_1[1])
            
            cv2.imshow("Rotate", imCrop)
            cv2.waitKey(0)

            x = yes_or_no("Is the image well rotated? (current angle of " + str(ang_1[1]) + "): ")
            if x == 0:
                dthet = input("Insert an angle of rotation (counterclockwise direction): ")
                if dthet != 0:
                    ang_1[1] = ang_1[1] + float(dthet)
                    hi = 1  
            if x == 1:
                rotate = 1
                ang_ent = ang_1[1]
                break 
        
        if rotate != 0:
            #print(ang_ent)
            #print(ang_1[1])
            ang_1[1] = ang_ent
            imCrop = rotate_image(im[int(rr[1]):int(rr[1]+rr[3]), int(rr[0]):int(rr[0]+rr[2])],ang_1[1])
        
    except:
        pass        
        
    return imCrop,ang_1[1]

def all_files(ext):
    # subfolders = [ f.path for f in os.scandir() if f.is_dir() ]
    names = []
    # for i in range(len(subfolders)):
    #     os.chdir(subfolders[i])
    #     for file in glob.glob(ext):
    #         names.append(file)
    #     return names
    for file in glob.glob(ext):
        names.append(file)
    return names
    
def profile(img_name):
    # Load some image
    im = io.imread(img_name)
    im.shape
    #im = np.rot90(im)
    #im = np.flip(im)

    # import warnings filter
    from warnings import simplefilter
    # ignore all future warnings
    simplefilter(action='ignore', category=FutureWarning)

    # Extract intensity values along some profile line
    p = profile_line(im, ((round(im.shape[1]/2)),0), (round(im.shape[1]/2),im.shape[0]))
    #print(p)
    p = np.flip(p)
    #print(p)
    # Extract values from image directly for comparison
    i =im[0:(im.shape[0]+1), (round(im.shape[1]/2))]
    ## #print(i)
    ## plt.plot(p)
    ## plt.ylabel('intensity')
    ## plt.xlabel('line path')
    ## plt.show(block=False)
    ## plt.pause(0.1)
    ## plt.close()
    return p

def increase_brightness(img, value=50):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def res_x(or_dir,jj,name):
    # or_dir = os.getcwd()
    names = all_files("Basler*")
    #print(names)
    crop_dir = "crop_d_"+name
    ## ## crop_dir = "crop_d_"+name
    ## ## try:
    ## ##     os.mkdir(crop_dir)
    ## ##     print("Directory created")
    ## ## except:
    ## ##     pass
    ## ## imcrop = []
    ## ## #cv2.imshow("asdf",imcrop[0])
    ## ## 
    ## ## #rr = coord(names[0],0.4)
    ii = np.zeros(len(names))
    ## ## x_rot = 0
    ## ## rotate = 1
    ## ## #pres_e = press()    
    ## ## 
    ## ## for i in range(len(names)):
    ## ##     
    ## ##     if i == 0:
    ## ##         rotate = 0 #ROTATE = 0 == ACTIVATE FIRST ROTATION
    ## ##         dthet = 0
    ## ##     elif i == 1:
    ## ##         #dthet = imcrop[3]
    ## ##         rotate = 1
    ## ##         
    ## ##     imcrop,dthet = crop(names[i],rr, rotate, dthet)
    ## ##     #imcrop = imcrop[0]
    ## ##     
    ## ##     os.chdir(crop_dir)
    ## ##     imcrop = increase_brightness(imcrop, value=20)
    ## ##     
    ## ##     cv2.imwrite('crop_'+str(i)+'.tif', cv2.cvtColor(imcrop, cv2.COLOR_BGR2GRAY))
    ## ##     # FIRST CROP, now we have to do the second internal crop
    ## ##     os.chdir("..")
    ## ## 
    ## ## os.chdir(crop_dir)
    ## ## names = all_files("crop*.tif")
    # print(names)
    #os.chdir("..")
    
    ## pd = []
    ## while len(pd) == 0:
    ##     
    ##     pd = input("Enter the pipette diameter in microns:")
## 
    ## input("Select in a rectangle the border of the pipette (Press ENTER) ")
## 
    ## x = 0
    ## while x!=1:
    ##     ##os.chdir(crop_dir)
    ##     rr = coord(names[0],2)
    ##     # print(rr[0]-rr[2])
    ##     pix = float(pd)/(abs(rr[3]))
    ##     # print(pix)
    ##     x = yes_or_no("Is the pipette edge well selected?")
    ##     #os.chdir("..")

    pix = 1/0.775 #um/px en objetivo x4
    
    #os.chdir(crop_dir)
    
    crop_dir = "crop_res"
    try:
        os.mkdir(crop_dir)
    except:
        pass
    
    x = 0
    
    input("Enclose the cell in a box (Press ENTER) ")
    while x == 0:
        rr = coord(names[0],10)
        # print(rr)
        # print(pix)
        # print(rr[2])
        #dia = (abs(rr[2]-rr[0])+abs(rr[3]-rr[1]))*0.5*pix
        dia = (rr[3]+rr[2])*0.5*pix
        print("The cell diameter is "+str(dia)+" micrometers")
        x = yes_or_no("Is the cell diameter well select?: ")


## 
    input("Select in a rectangle the constriction width (Press ENTER) ")
## 
    x = 0
    while x!=1:
        ##os.chdir(crop_dir)
        rr = coord(names[0],10)
        # print(rr[0]-rr[2])
        wch = abs(rr[3])*pix
        # print(pix)
        print("The constriction width is "+str(wch)+" micrometers")
        x = yes_or_no("Is the constriction width well selected?")
        #os.chdir("..")

    bch = input("Enter the number of blocked channels: ")

    x = 0
    
    while x == 0:
        #pres_e = press()
        input("Select the inside of the pipette (Press ENTER)")
        rr = coord(names[0],10)
        a = []
        aa = []
        
        for i in range(len(names)):    
            
        
            imcrop,dthet = crop(names[i],rr, 1, 0)
            
            os.chdir(crop_dir)
            cv2.imwrite("res_"+names[i], cv2.cvtColor(imcrop, cv2.COLOR_BGR2GRAY))               
            
            

            a = profile("res_"+names[i])
            #print(a)
            m = min(a)
            iih = [h for h, j in enumerate(a) if j == m]
            ii[i] = iih[0]
            os.chdir("..")

        ## aa = [-1*(i-ii[0])*pix/(float(pd)/2) for i in ii] #AL/RC
        aa = [-1*(i-ii[0])*pix for i in ii] #AL/RC
        
        jh = 0
        # pres_ee = []
        # aaa = []
        
        # for item in aa:
        #     if item >= 0:
        #         if item == aa[np.argmax(aa)]:
        #             continue
        #             #break
        #         else:
        #             aaa = np.append(aaa, item)
        #             pres_ee = np.append(pres_ee,pres_e[jh])
        #     jh=jh+1
    
        # plt.scatter(pres_e, aa, alpha=0.4)
        # plt.plot(pres_e, aa, 'r')
        # plt.show() 
        # print(aa)
        hz = 0.02 #time between frames in seconds
        xx = list(range(0,len(aa)))
        xx = [x*hz for x in xx]
        # print(xx)
        

        plt.scatter(xx, aa, alpha=0.4)
        plt.plot(xx, aa, 'r')
        plt.xlabel("Time [s]")
        plt.ylabel("Aspirated Length ($A_L$) [$\mu m$]")
        plt.show()
        
        #Rp=float(pd)/2
        
        ## the_e = []
        ## plz_e = []
        ## #print(pres_e)
        ## pres_ex, aa, the_e, plz_e = res_an(pres_e,aa,dia, Rp)
        x = yes_or_no("Is the analysis well done?: ")
    
    
    os.chdir(or_dir)
    
    try:
        os.mkdir("Results")
    except:
        pass 

    os.chdir("Results")

    #prese = np.array([pres_e]).T
    #aaa = np.array([aa]).T
    #print(prese)
    #print(aaa)
    #save = []
    jj=0
    
    with open(name+'.txt', 'w') as f:
        for item in aa:
            #save.append(pres_e[jj], item)
            f.write("%s %s\n" % (xx[jj] ,item))
            jj=jj+1
            
    with open("mec_res"+'.txt', 'a') as f:
        #save.append(pres_e[jj], item)
        f.write(name+ " %s %s %s\n" % (dia, wch, bch))
    #print(save)
    #print(or_dir)
    os.chdir(or_dir)
    return aa

def all_dir():
    or_dir = os.getcwd()
    subfolders = [ f.path for f in os.scandir(or_dir) if f.is_dir() ]
    subfolders = [ x for x in subfolders if "exp_" in x ]
    return subfolders


def std(dat):
    mean = np.mean(dat)
    std  = np.std(dat)


def plot_box():
    # --- Your data, e.g. results per algorithm:
    data1 = [5,5,4,3,3,5]
    data2 = [6,6,4,6,8,5]
    data3 = [7,8,4,5,8,2]
    data4 = [6,9,3,6,8,4]
    data6 = [17,8,4,5,8,1]
    data7 = [6,19,3,6,1,1]
    
    
    # --- Combining your data:
    data_group1 = [data1, data2, data6]
    data_group2 = [data3, data4, data7]
    data_group3 = [data1, data1, data1]
    data_group4 = [data2, data2, data2]
    data_group5 = [data2, data2, data2]
    
    data_groups = [data_group1, data_group2, data_group3] #, data_group4] #, data_group5]
    
    # --- Labels for your data:
    labels_list = ['a','b', 'c']
    width       = 0.3
    xlocations  = [ x*((1+ len(data_groups))*width) for x in range(len(data_group1)) ]
    
    symbol      = 'r+'
    ymin        = min ( [ val  for dg in data_groups  for data in dg for val in data ] )*0.8
    ymax        = max ( [ val  for dg in data_groups  for data in dg for val in data ])*1.2
    
    ax = plt.gca()
    ax.set_ylim(ymin,ymax)
    
    ax.grid(True, linestyle='dotted')
    ax.set_axisbelow(True)
    
    plt.xlabel('X axis label')
    plt.ylabel('Y axis label')
    plt.title('title')
    
    space = len(data_groups)/2
    offset = len(data_groups)/2
    
    
    ax.set_xticks( xlocations )
    ax.set_xticklabels( labels_list, rotation=0 )
    # --- Offset the positions per group:
    
    group_positions = []
    for num, dg in enumerate(data_groups):    
        _off = (0 - space + (0.5+num))
        #print(_off)
        group_positions.append([x-_off*(width+0.01) for x in xlocations])
    green_diamond = dict(markerfacecolor='b', marker='D')
    
    for dg, pos in zip(data_groups, group_positions):
        plt.boxplot(dg, 
        #            sym=symbol,
        #            labels=['']*len(labels_list),
                    labels=['']*len(labels_list),           
                    positions=pos, 
                    widths=width,
                    #flierprops = green_diamond,
                    #showfliers= False, 
        #           notch=False,  
        #           vert=False, 
                   whis=1.5,
        #           bootstrap=None, 
        #           usermedians=None, 
        #           conf_intervals=None,
        #           patch_artist=False,
                    )
        
    plt.show()

if __name__ == "__main__":
    # res = res_x()
    # plt.plot(res)
    # plt.show()
    
    
    or_dir = os.getcwd()
    subfolders = all_dir()
    i = 1
    
    for subf in subfolders:
        
        cont =1
        while cont == 1:
            try:
                nxt = status()
                #print(subf)
            except:
                input(" All the tests have been done!! ")
                cont = 0
                break
            
            name = nxt[0]
            #print(name)
            #print(subf)
            os.chdir('exp_'+name.split('_')[-1])
            res = res_x(or_dir,i,name)
            i=i+1
            cont = 0
            cont = yes_or_no("Do you wanna continue with the next analysis?")   
        
        if cont == 0:
            input(" #### See you later!! #### ")
            break
        
    os.chdir(or_dir) 
