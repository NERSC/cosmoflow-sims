import random
import time
import math
import subprocess
import multiprocessing
import os

def func(argus):
    omi = argus[0]
    sii = argus[1]
    nsi = argus[2]
    om = str(round(omi, 3))
    si = str(round(sii, 3))
    ns = str(round(nsi, 3))
    #print omi, sii

    tfile = "ics_template.conf"  ## read in template config file
    hdffilename = "ics_"+om+"_"+si+"_"+ns+".hdf5"
    if os.path.exists(hdffilename) and os.path.getsize(hdffilename)>10300000000: 
        #print "done this one"
        return
    else:
        print "***********", omi, sii, nsi
        outfilename = "ics_"+om+"_"+si+"_"+ns+".conf" ## make the config file name for this combination of cosmo params
        outfile = open(outfilename, "w")
        for line in open(tfile):
            
            if "Omega_m" in line:
                print >> outfile, "Omega_m                 = "+om
            elif "sigma_8" in line:
                print >> outfile, "sigma_8                 = "+si
            elif "nspec" in line:
                print >> outfile, "nspec                   = "+ns
            elif "filename" in line: 
                print >> outfile, "filename                = "+hdffilename
            elif "seed" in line:
                print >> outfile, "seed[9]                 = "+str(random.randrange(30000,40000))
            else:
                print >> outfile, line[:-1]

        outfile.close()
    
    
        ##########3 Now run MUSIC on this!
        cmd = ['../MUSIC', outfilename]
        print cmd
        
        q = subprocess.Popen(cmd)
        q.wait()
    
    

#######################################
if __name__ == '__main__':
    ## get random params for omM and si8
    random.seed(18885294) ### have this be repeatably random! Note that this is for the param values, NOT the random initial conditions


    nsamples = 4 ## How many simulations are we going to make? 
    oms, sis, nss = [], [], []
    for i in range(0, nsamples): ### defining the ranges for the simulation parameters
        r1 = random.randrange(2500, 3500) ## Om_m 0.25 - 0.35
        r2 = random.randrange(7800, 9500) ## Si_8 0.78 - 0.95
        r3 = random.randrange(9000, 10000) ## Ns 0.9 - 1.0

        oms.append(r1/10000.) ## taking the params down to the correct range/number of decimal places
        sis.append(r2/10000.)
        nss.append(r3/10000.)

    
    ### check if this file already exists, delete it if too small
    ct = 0
    for i in range(len(oms)):
        
        om = str(round(oms[i], 3))
        si = str(round(sis[i], 3))
        ns = str(round(nss[i], 3))
        hdffilename = "ics_"+om+"_"+si+"_"+ns+".hdf5"
        if os.path.exists(hdffilename):
            if os.path.getsize(hdffilename)>10300000000:  ### this is about the size of a successful run
                print i
            else:
                print "file size", os.path.getsize(hdffilename)
                os.remove(hdffilename)
        else:
            print om, si, ns 
            ct +=1
    print "need to run: ", ct, "more sims! "

    
    ### run this in parallel - each worker in the pool will run one set of omM/si8 params
    argus = zip(oms, sis, nss) 
    print len(oms)
    pool = multiprocessing.Pool(1)  ## 20 processes is about as many as you'd want to run on a single node interactively. 
    pool.map(func, argus)
    
    

