import numpy as np
import os
#import io

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
            
            
nume=4
name_inp = "fem_cfd_"+str(nume)+".inp"
name_cont= "fem_cfd_cont.inp"


file_inp = open(name_inp, 'r')
file_con = open(name_cont, 'r')

li_re = file_inp.readlines()
li_co = file_con.readlines()


s1_l = "** Name: s1   Type: Pressure Using Field: s1"
s2_l = "** Name: s2   Type: Pressure Using Field: s2"
s3_l = "** Name: s3   Type: Pressure Using Field: s3"
out_l = "** OUTPUT REQUESTS"

s1_r = search_string_in_file(name_inp,s1_l)[0][0]
s2_r= search_string_in_file(name_inp,s2_l)[0][0]
s3_r= search_string_in_file(name_inp,s3_l)[0][0]
out_r= search_string_in_file(name_inp,out_l)[0][0]

li_re[s1_r] = ' '.join(li_re[s1_r].split("\n"))+", follower=yes \n"
li_re[s2_r] = ' '.join(li_re[s2_r].split("\n"))+", follower=yes \n"
li_re[s3_r] = ' '.join(li_re[s3_r].split("\n"))+", follower=yes \n"

x = np.zeros(s2_r-1-(s1_r+1))
y = np.zeros(s3_r-1-(s2_r+1))
z = np.zeros(out_r-2-(s3_r+1))

j=0
for i in range(s1_r+1, s2_r-1):
    li_re[i] = li_re[i].replace("P", "TRVEC")
    li_re[i] = li_re[i][:-1]
    li_re[i] = li_re[i][:-1] +", 1.0, 0.0, 0.0\n"
    #print(li_re[i])
    #break
    x[j]=float(li_re[i].split(", ")[2])
    j=j+1

j=0
for i in range(s2_r+1, s3_r-1):
    li_re[i] = li_re[i].replace("P", "TRVEC")
    li_re[i] = li_re[i][:-1]
    li_re[i] = li_re[i][:-1] +", 0.0, 1.0, 0.0\n"
    y[j]=float(li_re[i].split(", ")[2])
    j=j+1

j=0
for i in range(s3_r+1, out_r-2):
    li_re[i] = li_re[i].replace("P", "TRVEC")
    li_re[i] = li_re[i][:-1]
    li_re[i] = li_re[i][:-1] +",0.0, 0.0, 1.0\n"
    #li_re[i] = ' '.join(li_re[i].split("\n"))
    #print(li_re[i])
    z[j]=float(li_re[i].split(",")[2])
    j=j+1

file_inp.close()
file_con.close()


f_inp = open(name_inp.split(".inp")[0]+"s.inp", "w")
###################

##################
#for i in range(len(li_re)):
for i in range(s1_r):
    n = f_inp.write(li_re[i])

n=f_inp.write("*Dload, op=NEW, follower=yes \n")

for i in range(len(x)):
    vec = np.array([x[i],y[i],z[i]])
    norm = np.linalg.norm(vec)

    n= f_inp.write(li_re[s1_r+1+i].split(",")[0]+","+li_re[s1_r+1+i].split(",")[1]+","+str(norm)+","+str(x[i]/norm)+","+str(y[i]/norm)+","+str(z[i]/norm)+"\n")

for i in range(len(li_re)-out_r):
    n= f_inp.write(li_re[i+out_r])

f_inp.close()

os.system("dos2unix "+name_inp.split(".inp")[0]+"s.inp")

################################
#### Write mod ####

f_inp = open(name_inp.split(".inp")[0]+"m.inp", "w")

n=f_inp.write("*Dload, op=MOD\n")

for i in range(len(x)):
    n=f_inp.write(li_re[s1_r-len(x)-1+i])

n=f_inp.write("*Dload, op=MOD, follower=yes \n")

for i in range(len(x)):
    vec = np.array([x[i],y[i],z[i]])
    norm = np.linalg.norm(vec)

    n= f_inp.write(li_re[s1_r+1+i].split(",")[0]+","+li_re[s1_r+1+i].split(",")[1]+","+str(norm)+","+str(x[i]/norm)+","+str(y[i]/norm)+","+str(z[i]/norm)+"\n")

for i in range(len(li_re)-out_r):
    n= f_inp.write(li_re[i+out_r])

f_inp.close()
os.system("dos2unix "+name_inp.split(".inp")[0]+"m.inp")

##

f_inp = open(name_inp.split(".inp")[0]+"x.inp", "w")

for i in range(14):
    n=f_inp.write(li_co[i])

n=f_inp.write("*Dload, op=MOD\n")

for i in range(len(x)):
    n=f_inp.write(li_re[s1_r-len(x)+i-1])

n=f_inp.write("*Dload, op=MOD, follower=yes \n")

for i in range(len(x)):
    vec = np.array([x[i],y[i],z[i]])
    norm = np.linalg.norm(vec)

    n= f_inp.write(li_re[s1_r+1+i].split(",")[0]+","+li_re[s1_r+1+i].split(",")[1]+","+str(norm)+","+str(x[i]/norm)+","+str(y[i]/norm)+","+str(z[i]/norm)+"\n")

for i in range(len(li_re)-out_r):
    n= f_inp.write(li_re[i+out_r])

f_inp.close()
#os.system("dos2unix "+name_inp.split(".inp")[0]+"x.inp")

with open(name_inp.split(".inp")[0]+"x.inp", "r") as file:
    filedata = file.read()


filedata=filedata.replace("*Restart, write, frequency=0","*Restart, write, overlay, frequency=1")
filedata=filedata.replace("*Output, field, variable=PRESELECT, time interval=0.0002","*Output, field, variable=PRESELECT, time interval=0.00001")
filedata=filedata.replace("*Output, history, variable=PRESELECT, time interval=0.0002", "*Output, history, variable=PRESELECT, time interval=0.00001")
filedata=filedata.replace("name=Step-2", "name=Step-"+str(nume))
filedata=filedata.replace("step=1","step="+str(nume-1))

with open(name_inp.split(".inp")[0]+"x.inp","w") as file:
    file.write(filedata)

os.system("dos2unix "+name_inp.split(".inp")[0]+"x.inp")
