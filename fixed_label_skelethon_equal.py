'''
fixed label GOS for class c_1
Last updates: August-11-2019
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
#from Symbolic_multi_AMI_new import *
#End
###################################

###################################
###########check_label#############
###################################
#Begin
def check_label(lbl):
  val=[]
  for i in range (0,len(lbl)):
    non_van=0
    for j in range (0,len(lbl[i])):
      if lbl[i][j]!=0:
        non_van=non_van+1
    val.append(non_van)
  return val  
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

diags_num=390

diags_1 = [181,204,210,268,349,353,379,413,444,489,502,538,552,588,612,628,630,633,650,668,669,670,671,676,683,701,770,817,831,875,894,895,896,912,973,986,993,997,1033,1034,1041,1061,1067,1140,1091,1107,1190,1194,1195,1232,1239,1245,1276,1278,1286,1288,1293,1294,1296,1305,1309,1320,1327,1329,1331,1337,1372,1375,1381,1388,1405,1409,1432,1433,1439,1445,1448,1454,1459,1468,1479,1484,1501,1506,1514,1519,1521,1527,1579,1594,1599,1610,1618,1620,1632,1643,1645,1661,1675,1677,1690,1714,1722,1732,1734,1736,1742,1754,1755,1760,1769,1770,1774,1777,1789,1790,1805,1812,1823,1832,1833,1836,1844,1865,1873,246,714,858,861,946,1004,1062,1084,1415,1424,1541,1556,1559,1624,1724,1783]
print '*****',diags_1
print len(diags_1)

#117=329
one_pair=[]
diags=[]
for i in range (0,len(diags_1)):
  
  for j in range (i+1,len(diags_1)):
    one_pair.append(diags_1[i])
    one_pair.append(diags_1[j])
    diags.append(one_pair)
    one_pair=[]
print diags
print '??????', len(diags)
    
#print len(diags)
impolites=[]

#impolites_JUNE_3=[8, 65, 55, 313]
#impolites_JUNE_11=[8, 65, 55, 313, 125, 113]
#impolites_JUNE_13=[8, 65, 55, 313, 125, 113, 153, 224]
#impolites_JUNE_14=[8, 65, 55, 313, 125, 113, 153, 224, 161, 366]
#impolites_JUNE_16=[8, 65, 55, 313, 125, 113, 153, 224, 161, 366, 192, 257]
#impolites_JUNE_18=[8, 65, 55, 313, 125, 113, 153, 224, 161, 366, 192, 257, 215, 51, 216, 205]
#impolites_JUNE_19=[8, 65, 55, 313, 125, 113, 153, 224, 161, 366, 192, 257, 215, 51, 216, 205, 236, 83]
#impolites_JULY_1=[8, 65, 55, 313, 125, 113, 153, 224, 161, 366, 192, 257, 215, 51, 216, 205, 236, 83, 1, 180, 2, 3]
#impolites_JULY_6=[8, 65, 55, 313, 125, 113, 153, 224, 161, 366, 192, 257, 215, 51, 216, 205, 236, 83, 1, 180, 2, 3, 13, 285]
file = open('equal_pairs_c_1_sweep_1.txt', 'w')
print 'len_pairs = ', len(diags)
M=6
repeat=150000
loop=True
tick=[]
imp_num=0
for pairs in range (0,len(diags)):
  loop=True
  
  for num_loop in range(0,16):
   
    for NUMBER in diags[pairs]:
      if num_loop==0:
        d_1=NUMBER
      if not loop:
        num_loop=41
        break
      file_name_ami_skelethon = 'ami_in_m_'+str(M)+'_num_'+str(NUMBER)
      with open(file_name_ami_skelethon,"rb") as fp:
        ami=pickle.load(fp)
      file_name_f_skelethon = 'f_m_'+str(M)+'_num_'+str(NUMBER)
      with open(file_name_f_skelethon,"rb") as fp:
        int_f=pickle.load(fp)
      int_freq_labels = deepcopy(ami)
      energy_signs=[1]*len(int_freq_labels)
      int_mnta_labels=deepcopy(int_freq_labels)
      label_char=check_label(ami)
      label_char.sort()

      
     
      if NUMBER not in impolites and loop:
        flag=True
      else:
        flag=False
      
      for NUMBER_comp in diags[pairs]:
        if NUMBER_comp not in impolites and flag and NUMBER!=NUMBER_comp:
        #if NUMBER!=NUMBER_comp and NUMBER not in tick and NUMBER_comp not in tick:
          #print 
          print NUMBER, NUMBER_comp
    
          file_name_ami_skelethon_p = 'ami_in_m_'+str(M)+'_num_'+str(NUMBER_comp)
          with open(file_name_ami_skelethon_p,"rb") as fp:
            ami_p=pickle.load(fp)
          label_char_p=check_label(ami_p)
          label_char_p.sort()
          print label_char
          print label_char_p
          if two_arr_eq(label_char,label_char_p)==False:   
            print 'impossible!' 
            flag=False
            imp_num=imp_num+1
            break  
          
          file_name_f_skelethon_p = 'f_m_'+str(M)+'_num_'+str(NUMBER_comp)
          with open(file_name_f_skelethon_p,"rb") as fp:
            int_f_p=pickle.load(fp)
          int_freq_labels_p = deepcopy(ami_p)
          energy_signs_p=[1]*len(int_freq_labels_p)
          int_mnta_labels_p=deepcopy(int_freq_labels_p)

          new_signs=deepcopy(energy_signs)
          new_freq=deepcopy(int_freq_labels)
          new_mnta=deepcopy(int_mnta_labels)

          for i in range(0,repeat):
        
            r=random()
            if r<0.5:
              coin1=randint(1,M)
              coin2=randint(1,M)
              if coin1!=coin2: #and valid(new_freq,coin1)!=1 and valid(new_freq,coin2)!=1:
                new_freq=deepcopy(freq_swap(new_freq,coin1,coin2))
                new_mnta=deepcopy(mnta_swap(new_mnta,coin1,coin2))  
            dec=dec_polite(int_freq_labels_p,int_mnta_labels_p,energy_signs_p,new_freq,new_mnta,new_signs,int_f,int_f_p)
            if dec==0:
              #print 'new_freq = ', new_freq
              #print 'new_mnta = ', new_mnta
              #print 'new_signs = ', new_signs
              print i
              impolites.append(NUMBER)
              impolites.append(NUMBER_comp)
              print impolites
              num_loop=41
              loop=False
              flag=False
              txt=str(NUMBER) + '\t' + str(NUMBER_comp) + '\n'
              file.write(txt)
              if NUMBER_comp!=d_1:
                tick.append(NUMBER_comp)
              if NUMBER!=d_1:
                tick.append(NUMBER)
              break
        
            r=random()
            if r<0.5:
              coin=randint(1,M)
              if valid(new_freq,coin)!=1:
                new_freq=deepcopy(freq_sign_chng(new_freq,coin)) 
                new_mnta=deepcopy(mnta_sign_chng(new_mnta,coin)) 
            dec=dec_polite(int_freq_labels_p,int_mnta_labels_p,energy_signs_p,new_freq,new_mnta,new_signs,int_f,int_f_p)
            if dec==0:
              #print 'new_freq = ', new_freq
              #print 'new_mnta = ', new_mnta
              #print 'new_signs = ', new_signs
              print i
              impolites.append(NUMBER)
              impolites.append(NUMBER_comp)
              print impolites
              num_loop=41
              loop=False
              flag=False
              txt=str(NUMBER) + '\t' + str(NUMBER_comp) + '\n'
              file.write(txt)
              if NUMBER_comp!=d_1:
                tick.append(NUMBER_comp)
              if NUMBER!=d_1:
                tick.append(NUMBER)
              break
  
            if r>=0.5:
              coin=randint(1,M)
              if valid(new_freq,coin)!=1:
                new_signs=mnta_shift(new_freq,new_signs,coin)
            dec=dec_polite(int_freq_labels_p,int_mnta_labels_p,energy_signs_p,new_freq,new_mnta,new_signs,int_f,int_f_p)
            #print new_freq
            #print new_mnta
            #print new_signs
            if dec==0:
              #print 'new_freq = ', new_freq
              #print 'new_mnta = ', new_mnta
              #print 'new_signs = ', new_signs
              print i
              impolites.append(NUMBER)
              impolites.append(NUMBER_comp)
              print impolites
              txt=str(NUMBER) + '\t' + str(NUMBER_comp) + '\n'
              file.write(txt)
              num_loop=41
              loop=False
              flag=False
              if NUMBER_comp!=d_1:
                tick.append(NUMBER_comp)
              if NUMBER!=d_1:
                tick.append(NUMBER)
              break  
print 'impolites = ', impolites
polites=[]

print 'imo_num = ', imp_num/16.0

#for i in diags:
  #if i not in impolites:
    #polites.append(i)
#print 'polites = ', polites 

'''
for i in range(0,len(polites)):
  file_name_G_sym = 'G_sym_m_'+str(M)+'_num_'+str(polites[i]) 
  with open(file_name_G_sym,"rb") as fp:
    g_sym_polite=pickle.load(fp)
  #print g_sym_polite
  file_name_polite_G_sym = 'polite_G_sym_m_'+str(M)+'_num_'+str(polites[i])
  with open(file_name_polite_G_sym,"wb") as fp:
    pickle.dump(g_sym_polite,fp)
#file_name_polite_G_sym = 'polite_G_sym_m_'+str(M)+'_num_'+str(3)
#with open(file_name_polite_G_sym,"rb") as fp:
    #g_sym_polite=pickle.load(fp)
#print g_sym_polite
'''
