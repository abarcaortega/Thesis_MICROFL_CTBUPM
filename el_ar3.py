import numpy as np
#from __future__ import print_function

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string, along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
    # Read all lines in the file one by one
        for line in read_obj:
        # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
            # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
                # Return list of tuples containing line numbers and lines where string is found
                return list_of_results



name = 'cfd_4'
name_inp=name+'.inp'
name_r = name+'.txt'
typ_s = "PART-1-1"#"FLUID-1"#'PART-1-1' #CFD-

res_inp = open(name_r, 'r')
li_re = res_inp.readlines()

se_r = '  Part Instance  Element ID        Type            Face  STRACTION, STRACTION1'
se1_r = '  Part Instance  Element ID        Type  Attached nodes'
se_r2 = '  Part Instance  Element ID        Type            Face  STRACTION, STRACTION2'
se_r3 = '  Part Instance  Element ID        Type            Face  STRACTION, STRACTION3'
se_pr = '  Part Instance     Node ID  Attached elements        PRESSURE'
se_prc= '  Part Instance     Node ID                   Orig. Coords                                     Def. Coords                 '

lse_r = search_string_in_file(name_r,se_r)[0][0]
lse_r1= search_string_in_file(name_r,se1_r)[0][0]
lse_r2= search_string_in_file(name_r,se_r2)[0][0]
lse_r3= search_string_in_file(name_r,se_r3)[0][0]
lse_pr= search_string_in_file(name_r,se_pr)[0][0]
lse_prc=search_string_in_file(name_r,se_prc)[0][0]

tt1 = []

for i in range(lse_r-lse_r1-4):
    tt1.append(li_re[i+lse_r1+1].split())
    tt1[i].remove(typ_s)
    tt1[i].remove('FC3D4')
    del(tt1[i][0])
    
    try:
        for j in range(len(tt1[i])+1):
            tt1[i][j]=tt1[i][j].split(":")[-1]
            tt1[i][j]=tt1[i][j].split(")")[0]
    except:
        pass
    tt1[i]=list(set(tt1[i]))
    #print(tt1[i])
    #break

tt = []
tt2= []
tt3= []
print("Starting...")
for i in range(len(tt1)):
    tt.append(li_re[i+lse_r+1].split())
    tt[i].remove(typ_s)
    tt[i].remove('FC3D4')
    #print(tt[i])

    tt2.append(li_re[i+lse_r2+1].split())
    tt2[i].remove(typ_s)
    tt2[i].remove('FC3D4')

    tt3.append(li_re[i+lse_r3+1].split())
    tt3[i].remove(typ_s)
    tt3[i].remove('FC3D4')

for xx in range(len(tt)):
    if tt[xx][1] == 'f3:1':
        del(tt1[xx][0])
    elif tt[xx][1] == 'f1:1':
        del(tt1[xx][3])
    elif tt[xx][1] == 'f2:1':
        del(tt1[xx][2])
    elif tt[xx][1] == 'f4:1':
        del(tt1[xx][1])

fin = np.zeros((len(tt),12))

for i in range(len(tt)):
    fin[i][0] = int(tt[i][0])
    fin[i][1] = int(tt1[i][0])
    fin[i][2] = int(tt1[i][1])
    fin[i][3] = int(tt1[i][2])  
    fin[i][4] = float(tt[i][-1]) ##TRACTION 1 IN FACE
    fin[i][5] = float(tt2[i][-1])
    fin[i][6] = float(tt3[i][-1])

### We have already a fine = ELEMENT ID | NODES OF FACE | TRACTION 1
### We need to calculate the area of that face, the centroid and the pressure

gap = 2+lse_prc

#inp = open(name_inp, 'r')
li_inp = li_re
coord_st = []

for i in range(len(fin)):
    
    for ix in range(lse_pr-lse_prc-6):
        if fin[i][1] == int(li_re[lse_prc+2+ix].split()[1]):
            x1 = float(li_re[lse_prc+2+ix].split()[2])
            y1 = float(li_re[lse_prc+2+ix].split()[3])
            z1 = float(li_re[lse_prc+2+ix].split()[4])
        elif fin[i][2] == int(li_re[lse_prc+2+ix].split()[1]):
            x2 = float(li_re[lse_prc+2+ix].split()[2])
            y2 = float(li_re[lse_prc+2+ix].split()[3])
            z2 = float(li_re[lse_prc+2+ix].split()[4])
        elif fin[i][3] == int(li_re[lse_prc+2+ix].split()[1]):
            x3 = float(li_re[lse_prc+2+ix].split()[2])
            y3 = float(li_re[lse_prc+2+ix].split()[3])
            z3 = float(li_re[lse_prc+2+ix].split()[4])
    
    #coord_st.append(li_inp[int(fin[i][1])+gap].split()[1:4]+li_inp[int(fin[i][2])+gap].split()[1:4]+li_inp[int(fin[i][3])+gap].split()[1:4])
    #for xx in range(len(coord_st[i])):
    #        coord_st[i][xx] = coord_st[i][xx].replace(",","")
    
    #A = [float(coord_st[i][0]),float(coord_st[i][1]),float(coord_st[i][2])]
    #B = [float(coord_st[i][3]),float(coord_st[i][4]),float(coord_st[i][5])]  
    #C = [float(coord_st[i][6]),float(coord_st[i][7]),float(coord_st[i][8])]
    A = [x1,y1,z1]
    B = [x2,y2,z2]
    C = [x3,y3,z3]
    AB = np.subtract(A,B)
    AC = np.subtract(A,C)
    fin[i][-4]= (np.linalg.norm(np.cross(AB,AC)))/2
    fin[i][-3] = (A[0]+B[0]+C[0])/3
    fin[i][-2] = (A[1]+B[1]+C[1])/3
    fin[i][-1] = (A[2]+B[2]+C[2])/3
    
    print(str(i+1)+" of "+ str(len(fin))+" || "+ str(round(((i+1) / float(len(fin)))*100,1))+"% done")

## fin = Element ID | Nodes of Face | Traction 1,2,3 | area | baricenter (x, y, z) |
#print("Done part 1")


#press = []
#
#for i in range(len(li_re)-lse_pr-3):
#    press.append(li_re[i+lse_pr+1].split())
#    press[i].remove(typ_s)
#
#
#i = 1
#n_pr = np.zeros((1,3))
#ii = 0
#
#i1 = 0
#i2 = 0
#i3 = 0
#
#for xx in range(len(fin)):
#
#    nod = fin[xx][1:4]
#
#    for i in range(len(li_re)-lse_pr-3):
#        n_id = li_re[lse_pr+i+1].split()[1]
#        #n_id2 = li_re[lse_pr+i+1].split()[2]
#        #n_id3 = li_re[lse_pr+i+1].split()[3]
#    
#        if int(n_id) == int(nod[0]):
#            n_pr[0][0] = li_re[lse_pr+i+1].split()[3]
#            i1 = 1
#        elif int(n_id) == int(nod[1]):
#            n_pr[0][1] = li_re[lse_pr+i+1].split()[3]
#            i2 = 1
#        elif int(n_id) == int(nod[2]):
#            n_pr[0][2] = li_re[lse_pr+i+1].split()[3]
#            i3 = 1
#
#        #print(n_pr)
#        
#        pr_av = float(np.mean(n_pr))
#        
#        if np.floor(np.mean((i1,i2,i3))) == 1:
#            ii+=1
#            i1 = 0
#            i2 = 0
#            i3 = 0
#            fin[xx][7] = pr_av
#            print(str(xx+1)+" of "+ str(len(fin))+" || "+ str(round(((xx+1) / float(len(fin)))*100,1))+"% done") 
#
## fin = Element ID | Nodes of Face | Traction 1,2,3 | MAIN PRESS | area | baricenter (x, y, z) |
a_fi = open("resu_"+name+".txt","w")
r_f1 = open("S1_"+name+".txt","w")
r_f2 = open("S2_"+name+".txt","w")
r_f3 = open("S3_"+name+".txt","w")

for i in range(len(fin)):
    n = a_fi.write(str(int(fin[i][0]))+" "+str(int(fin[i][1]))+ \
            " "+str(int(fin[i][2]))+" "+str(int(fin[i][3]))+ \
            " "+str(float(fin[i][4]))+" "+str(float(fin[i][5]))+" "+str(float(fin[i][6]))+ \
            " "+str(float(fin[i][7]))+" "+str(float(fin[i][8]))+" "+str(float(fin[i][9]))+ \
            " "+str(float(fin[i][10]))+" "+str(float(fin[i][11]))+"\n")

for i in range(len(fin)):
    n1 = r_f1.write(str(float(fin[i][9]))+" "+str(float(fin[i][10]))+ \
            " "+str(float(fin[i][11]))+" "+str(float(fin[i][4]))+"\n")

for i in range(len(fin)):
    n2 = r_f2.write(str(float(fin[i][9]))+" "+str(float(fin[i][10]))+ \
            " "+str(float(fin[i][11]))+" "+str(float(fin[i][5]))+"\n")

for i in range(len(fin)):
    n3 = r_f3.write(str(float(fin[i][9]))+" "+str(float(fin[i][10]))+ \
            " "+str(float(fin[i][11]))+" "+str(float(fin[i][6]))+"\n")

    
#for i in range(len(fin)):
#    n = a_fi.write(str(fin[i][0])+" "+str(fin[i][1])+" "+str(fin[i][2])+" "+ \
#            str(fin[i][3])+" "+str(fin[i][4])+" "+str(fin[i][5])+" "+ \
#            str(fin[i][6])+" "+str(fin[i][7]+" "+str(fin[i][8])+" "+ \
#            str(fin[i][9])+" "+str(fin[i][10])+" "+str(fin[i][11])+"\n")
#
a_fi.close() 
r_f1.close()
r_f2.close()
r_f3.close()

######

print("Process finished!")
