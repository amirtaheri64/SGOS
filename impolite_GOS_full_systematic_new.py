'''
Polite AMI+diagMC for the
self-energy up to the second order

Last updates: July-29-1019
'''

###################################
##########Import libraries#########
###################################
#Begin
from random import *
import pickle
from math import *
import numpy as np
from copy import deepcopy
from itertools import permutations 
#from Symbolic_multi_AMI_new import *
#End
###################################

###################################
#######Frequency sign chanage######
###################################
#Begin
def freq_sign_chng(g_freq,p): 
  val=deepcopy(g_freq)
  #print 'val_init = ', val
  for i_g in range (0,len(val)):
    val[i_g][p-1]=-val[i_g][p-1]
  #print 'init=',g_freq
  #print 'final=',val
  return val 
#End
###################################

###################################
#######Momentum sign chanage#######
###################################
#Begin
def mnta_sign_chng(g_mnta,p): 
  val=deepcopy(g_mnta)
  #print 'val_init = ', val
  for i_g in range (0,len(val)):
    val[i_g][p-1]=-val[i_g][p-1]
  #print 'init=',g_mnta
  #print 'final=',val
  return val 
#End
###################################

###################################
#######Momentum shift by pi########
###################################
#Begin
def mnta_shift(g_freq,signs,p):
  val=signs
  for i_g in range (0,len(val)):
    if g_freq[i_g][p-1]!=0:
      val[i_g]=-val[i_g]
  #print 'new_signs=', val
  return val
#End
###################################

###################################
#########Frequency swap############
###################################
#Begin
def freq_swap(g_freq,p1,p2):
  val_freq=deepcopy(g_freq)
  for i_g in range(0,len(val_freq)):
    temp=g_freq[i_g][p1-1]
    g_freq[i_g][p1-1]=g_freq[i_g][p2-1]
    g_freq[i_g][p2-1]=temp
  return g_freq
#End
###################################

###################################
#########M#omentum swap############
###################################
#Begin
def mnta_swap(g_mnta,p1,p2):
  val_mnta=deepcopy(g_mnta)
  for i_g in range(0,len(val_mnta)):
    temp=g_mnta[i_g][p1-1]
    g_mnta[i_g][p1-1]=g_mnta[i_g][p2-1]
    g_mnta[i_g][p2-1]=temp
  return g_mnta
#End
###################################


############################
###two arrays are equal?####
############################
#Begin
def two_arr_eq(r1,r2):
  val = True
  for i in range (0, len(r1)):
    if r1[i] != r2[i]:
      val = False
  return val
#End
############################

########################################################
##Comarison of two arrays considering the overall sign##
########################################################
#Begin      
def arr_comp_new(r1, r2):
  ovl_sgn = 1
  r2_new = [None]*len(r2)
  val = False
  if two_arr_eq(r1,r2):
    val = True
    ovl_sgn = 1
  for i in range(0,len(r2)):
    r2_new[i] = -r2[i] 
  if two_arr_eq(r1,r2_new):
    val = True
    ovl_sgn = ovl_sgn*(-1)
  
  return val,ovl_sgn 
#End
########################################################

###################################
###########Green comp##############
###################################
#Begin
def g_comp(g1,g2):
  #flag_g_comp=True
  ovl_sgn=1
  out=[]
  g2_copy=deepcopy(g2)
  rel_sgn=[]
  count=0
  #print arr_comp_new(g1[0],g2[1])
  
  for i in range (0,len(g1)):
    #print 'g1 = ', g1[i]
    
      for j in range (0,len(g2_copy)):
       
        if arr_comp_new(g1[i],g2_copy[j])[0]:
          count=count+1
          out.append(g2_copy[j])
          flag_g_comp=True
          ovl_sgn=ovl_sgn*arr_comp_new(g1[i],g2_copy[j])[1]
          
          rel_sgn.append(arr_comp_new(g1[i],g2_copy[j])[1])
          g2_copy[j]=[0]*len(g2_copy[0])
          break
        #else: 
          #flag_g_comp=False
  #if len(out)==len(g2_copy):
    #val=True
  #print 'count = ', count
  if count==len(g2_copy):
    val=True
  else:
    val=False
  return val,ovl_sgn,rel_sgn
#End
###################################

###################################
######Is transformation valid?#####
###################################
def valid(g_freq,p):
  count_p=0
  for i in range(0,len(g_freq)):
    if g_freq[i][p-1]!=0:
      count_p=count_p+1
  #print count_p
  return count_p
#End
###################################  

'''
###################################
#########Decision func#############
###################################
#Begin
def dec_polite(int_freq,int_mnta,int_signs,NEW_freq,NEW_mnta,NEW_signs,int_num_loop,NEW_num_loop):
  polite=1
  flag=True
  overal_sign_freq=1
  comp=g_comp(NEW_freq, int_freq)
    #print comp
  if comp[0]==False:
    flag=False
  overal_sign_freq=comp[1]*overal_sign_freq*((-1)**(int_num_loop-NEW_num_loop))
  #print 'flag_freq= ', flag
  #print '*****' , overal_sign_freq

  #print 'NEW_mnta = ', NEW_mnta
  #print 'int_mnta = ', int_mnta
  if flag:
    comp=g_comp(NEW_mnta, int_mnta)
    #print comp
    if comp==False:
      flag=False
  #print 'flag_freq_mnta= ', flag
  check_freq=deepcopy(NEW_freq)
  if flag:
    #comp=arr_comp_new(int_signs,NEW_signs)
    sign_final=1
    for i in range (0,len(NEW_signs)):
      sign_final=sign_final*NEW_signs[i]
      for j in range (0, len(NEW_freq[i])):
        check_freq[i][j]=NEW_signs[i]*check_freq[i][j]
    #print 'sign_final = ', sign_final
    #print 'overal_sign = ', overal_sign_freq
    #print 'check_freq = ', check_freq
    comp=g_comp(check_freq,int_freq)
    #print 'comp = ', comp
    if sign_final==overal_sign_freq==-1 and comp[0] and comp[1]==1 and comp[2]==[1]*len(comp[2]) :
      #print 'Impolite'
      polite=0
  return polite
#End
###################################

'''
###################################
#########Decision func#############
###################################
#Begin
def dec_polite(int_freq,int_mnta,int_signs,NEW_freq,NEW_mnta,NEW_signs,int_num_loop,NEW_num_loop):
  polite=1
  flag=True
  overal_sign_freq=1
  comp=g_comp(NEW_freq, int_freq)
    #print comp
  if comp[0]==False:
    flag=False
  overal_sign_freq=comp[1]*overal_sign_freq*((-1)**(int_num_loop-NEW_num_loop))
  #print 'flag_freq= ', flag
  #print overal_sign_freq

  if flag:
    comp=g_comp(NEW_mnta, int_mnta)
    #print comp
    if comp[0]==False:
      flag=False
  #print 'flag_freq_mnta= ', flag
  check_freq=deepcopy(NEW_freq)
  if flag:
    #comp=arr_comp_new(int_signs,NEW_signs)
    sign_final=1
    for i in range (0,len(NEW_signs)):
      sign_final=sign_final*NEW_signs[i]
      for j in range (0, len(NEW_freq[i])):
        check_freq[i][j]=NEW_signs[i]*check_freq[i][j]
    #print 'sign_final = ', sign_final
    #print 'overal_sign = ', overal_sign_freq
    #print 'check_freq = ', check_freq
    comp=g_comp(check_freq,int_freq)
    #print 'comp = ', comp
    if overal_sign_freq==1 and comp[0] and comp[1]==1 and comp[2]==[1]*len(comp[2]) :
      #print 'Impolite'
      polite=0
  return polite
#End
###################################

M=4
num_ind=M
#num_swap=3

#####################################
#Genrarate all the frequency choices#
#####################################
#Begin

a=[1,2,3]
sign_pm=[1]*len(a)
out=[]
for i1 in range (0,2):
  a[0]=a[0]*sign_pm[0]
  sign_pm[0]=sign_pm[0]*(-1)
  for i2 in range (0,2):
    a[1]=a[1]*sign_pm[1]
    sign_pm[1]=sign_pm[1]*(-1)
    for i3 in range (0,2):
      a[2]=a[2]*sign_pm[2]
      sign_pm[2]=sign_pm[2]*(-1)
      out.append(deepcopy(a))
 

a=[1,2,3,4]
sign=[1]*len(a)
out=[]
for i1 in range (0,2):
  a[0]=a[0]*sign[0]
  sign[0]=sign[0]*(-1)
  for i2 in range (0,2):
    a[1]=a[1]*sign[1]
    sign[1]=sign[1]*(-1)
    for i3 in range (0,2):
      a[2]=a[2]*sign[2]
      sign[2]=sign[2]*(-1)
      for i4 in range (0,2):
        a[3]=a[3]*sign[3]
        sign[3]=sign[3]*(-1)
        out.append(deepcopy(a))

'''
a=[1,2,3,4,5,6]
sign=[1]*len(a)
out=[]
for i1 in range (0,2):
  a[0]=a[0]*sign[0]
  sign[0]=sign[0]*(-1)
  for i2 in range (0,2):
    a[1]=a[1]*sign[1]
    sign[1]=sign[1]*(-1)
    for i3 in range (0,2):
      a[2]=a[2]*sign[2]
      sign[2]=sign[2]*(-1)
      for i4 in range (0,2):
        a[3]=a[3]*sign[3]
        sign[3]=sign[3]*(-1)
        for i5 in range (0,2):
          a[4]=a[4]*sign[4]
          sign[4]=sign[4]*(-1)
          for i6 in range (0,2):
            a[5]=a[5]*sign[5]
            sign[5]=sign[5]*(-1)
            out.append(deepcopy(a))
            #print a 
'''
print 'out = ', out
print 'len(out) = ', len(out) 

#End
######################################

######################################
##############All permutations########
######################################
#Begin
per = list(permutations(range(1, M+1))) 
print 'per = ', per 
print 'len(per) = ', len(per)
#End
######################################
diags=[[26,32]]  
count=0    
impolites=[]
count_loop=0
for pairs in range (0,len(diags)):
  loop=True
  for num_loop in range(0,1):
    for NUMBER in diags[pairs]:
      if not loop:
        num_loop=41
        break
      file_name_ami_skelethon = 'ami_in_m_'+str(M)+'_num_'+str(NUMBER)
      with open(file_name_ami_skelethon,"rb") as fp:
        ami=pickle.load(fp)
      file_name_f_skelethon = 'f_m_'+str(M)+'_num_'+str(NUMBER)
      with open(file_name_f_skelethon,"rb") as fp:
        int_f=pickle.load(fp)
      #ami = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[1,-1,0,1],[0,-1,1,1]]
      int_freq_labels = deepcopy(ami)
      energy_signs=[1]*len(int_freq_labels)
      int_mnta_labels=deepcopy(int_freq_labels)
      if NUMBER not in impolites and loop:
        flag=True
      else:
        flag=False
      for NUMBER_comp in diags[pairs]:
        if not loop:
          num_loop=41
          break
        if NUMBER_comp not in impolites and flag and NUMBER!=NUMBER_comp:
          #print 
          print NUMBER, NUMBER_comp
          
          file_name_ami_skelethon_p = 'ami_in_m_'+str(M)+'_num_'+str(NUMBER_comp)
          with open(file_name_ami_skelethon_p,"rb") as fp:
            ami_p=pickle.load(fp)
          file_name_f_skelethon_p = 'f_m_'+str(M)+'_num_'+str(NUMBER_comp)
          with open(file_name_f_skelethon_p,"rb") as fp:
            int_f_p=pickle.load(fp)
          #ami_p=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[-1,1,0,1],[0,1,-1,1]]
          int_freq_labels_p = deepcopy(ami_p)
          energy_signs_p=[1]*len(int_freq_labels_p)
          int_mnta_labels_p=deepcopy(int_freq_labels_p)

          new_signs=deepcopy(energy_signs)
          new_freq=deepcopy(int_freq_labels)
          new_mnta=deepcopy(int_mnta_labels)
          #print 'old_freq = ', new_freq
          #print 'old_mnta = ', new_mnta
          #print 'old_signs = ', new_signs
          for i_out in range (0,len(out)):
            if not loop:
              num_loop=41
              break
            print 'i_out = ', i_out 
            new_signs=deepcopy(energy_signs)
            new_freq=deepcopy(int_freq_labels)
            new_mnta=deepcopy(int_mnta_labels)
            #print '_____'
            freq_choice=out[i_out]
            for i_freq_choice in range (0,len(freq_choice)):
              if freq_choice[i_freq_choice]<0:
                if valid(new_freq,-freq_choice[i_freq_choice])!=1:
                  new_freq=deepcopy(freq_sign_chng(new_freq,-freq_choice[i_freq_choice])) 
                  new_mnta=deepcopy(mnta_sign_chng(new_mnta,-freq_choice[i_freq_choice])) 
            #print 'freq_choice = ', freq_choice
            #print 'new_freq = ', new_freq
            #print 'new_mnta = ', new_mnta
            #print 'new_signs = ', new_signs
            #print   
            dec=dec_polite(int_freq_labels_p,int_mnta_labels_p,energy_signs_p,new_freq,new_mnta,new_signs,int_f,int_f_p)
            if dec==0:
              #print 'new_freq = ', new_freq
              #print 'new_mnta = ', new_mnta
              #print 'new_signs = ', new_signs
              #print i
              impolites.append(NUMBER)
              impolites.append(NUMBER_comp)
              print impolites
              print 'number of tries = ', count_loop
              num_loop=41
              loop=False
              flag=False
              txt=str(NUMBER) + '\t' + str(NUMBER_comp) + '\n'
              #file.write(txt)
              #print new_freq
              #print new_signs
              break
              #print 'new_freq = ', new_freq
              #print 'new_signs = ', new_signs
            new_signs_copy=deepcopy(new_signs)
            new_freq_copy=deepcopy(new_freq)
            new_mnta_copy=deepcopy(new_mnta)
            for i_out_sh in range (0,len(out)):
              if not loop:
                num_loop=41
                break
              #print 'i_out_sh = ', i_out_sh
              new_signs=deepcopy(new_signs_copy)
              new_freq=deepcopy(new_freq_copy)
              new_mnta=deepcopy(new_mnta_copy) 
              #count_loop = count_loop+1
              count=count+1
              sh_choice=out[i_out_sh]
              #print '****'
              for i_sh_choice in range (0,len(sh_choice)):
                if sh_choice[i_sh_choice]<0:
                  if valid(new_freq,-sh_choice[i_sh_choice])!=1:
                    #print '?????'
                    new_signs=mnta_shift(new_freq,new_signs,-sh_choice[i_sh_choice])
              #print 'sh_choice = ', sh_choice
              #print 'new_freq = ', new_freq
              #print 'new_mnta = ', new_mnta
              #print 'new_signs = ', new_signs
              dec=dec_polite(int_freq_labels_p,int_mnta_labels_p,energy_signs_p,new_freq,new_mnta,new_signs,int_f,int_f_p)
              if dec==0:
                #print 'new_freq = ', new_freq
                #print 'new_mnta = ', new_mnta
                #print 'new_signs = ', new_signs
                #print i
                impolites.append(NUMBER)
                impolites.append(NUMBER_comp)
                print impolites
                print 'number of tries = ', count_loop
                num_loop=41
                loop=False
                flag=False
                txt=str(NUMBER) + '\t' + str(NUMBER_comp) + '\n'
                #print new_freq
                #print new_signs
                #file.write(txt)
                break 
              #new_signs=deepcopy(new_signs_copy)
              #new_freq=deepcopy(new_freq_copy)
              #new_mnta=deepcopy(new_mnta_copy) 
              new_signs_copy_1=deepcopy(new_signs)
              new_freq_copy_1=deepcopy(new_freq)
              new_mnta_copy_1=deepcopy(new_mnta)
              
              for i_swap in range (0,len(per)):
                if not loop:
                  num_loop=41
                  break
                new_signs = deepcopy(new_signs_copy_1)
                new_freq = deepcopy(new_freq_copy_1)
                new_mnta = deepcopy(new_mnta_copy_1)
                count_loop = count_loop+1
                new_freq_per = deepcopy(new_freq)
                new_mnta_per = deepcopy(new_mnta)
                for i in range (0,len(new_freq)):
                  for j in range (0,len(new_freq[i])-1):
                    new_freq_per[i][j]=None
                    new_freq_per[i][j]=None
                per_choice = per[i_swap]
                for i_per_choice in range (0,len(per_choice)):
                  if per_choice[i_per_choice]==i_per_choice+1:
                    for i in range (0,len(new_freq_per)):
                      new_freq_per[i][i_per_choice] = new_freq[i][i_per_choice]
                  else: 
                    for i in range (0,len(new_freq_per)):
                      new_freq_per[i][i_per_choice] = new_freq[i][per_choice[i_per_choice]-1]
                
                new_freq=deepcopy(new_freq_per)
                new_mnta=deepcopy(new_freq_per)  
                #print 'new_freq = ', new_freq
                #print 'new_mnta = ', new_mnta
                #print 'new_signs = ', new_signs
                dec=dec_polite(int_freq_labels_p,int_mnta_labels_p,energy_signs_p,new_freq,new_mnta,new_signs,int_f,int_f_p)
                
                if dec==0:
                  #print 'new_freq = ', new_freq
                  #print 'new_mnta = ', new_mnta
                  #print 'new_signs = ', new_signs
                
                  impolites.append(NUMBER)
                  impolites.append(NUMBER_comp)
                  print impolites
                  print 'number of tries = ', count_loop
                  num_loop=41
                  loop=False
                  flag=False
                  txt=str(NUMBER) + '\t' + str(NUMBER_comp) + '\n'
                  print 'freq choice = ', freq_choice
                  print 'sh_choice = ', sh_choice
                  print 'per_choice = ', per_choice
                  #file.write(txt)
                  break
                #new_signs=deepcopy(new_signs_copy_1)
                #new_freq=deepcopy(new_freq_copy_1)
                #new_mnta=deepcopy(new_mnta_copy_1)
                 
              '''
              for i_per in range (0,len(per)):
                count_loop = count_loop+1
                per_choice=per[i_per]
                b=[]
                for i_per_choice in range (0,len(per_choice)):
                  #if per_choice[i_per_choice]!=i_per_choice+1:
                  
                  if per_choice[i_per_choice] not in b and i_per_choice+1 not in b:
                    new_freq=deepcopy(freq_swap(new_freq,per_choice[i_per_choice],i_per_choice+1))
                    new_mnta=deepcopy(mnta_swap(new_mnta,per_choice[i_per_choice],i_per_choice+1))  
                dec=dec_polite(int_freq_labels_p,int_mnta_labels_p,energy_signs_p,new_freq,new_mnta,new_signs,int_f,int_f_p)
                b.append(per_choice[i_per_choice])
                b.append(i_per_choice+1)
                if dec==0:
                  #print 'new_freq = ', new_freq
                  #print 'new_mnta = ', new_mnta
                  #print 'new_signs = ', new_signs
                
                  impolites.append(NUMBER)
                  impolites.append(NUMBER_comp)
                  print impolites
                  print 'number of tries = ', count_loop
                  num_loop=41
                  loop=False
                  flag=False
                  txt=str(NUMBER) + '\t' + str(NUMBER_comp) + '\n'
                  #file.write(txt)
                  break
                new_signs=deepcopy(new_signs_copy_1)
                new_freq=deepcopy(new_freq_copy_1)
                new_mnta=deepcopy(new_mnta_copy_1) 
                '''
#print 'new_freq = ', new_freq
#print 'new_mnta = ', new_mnta
#print 'new_signs = ', new_signs
print 'impolites = ', impolites
print 'count_loop = ', count_loop
print count

   

