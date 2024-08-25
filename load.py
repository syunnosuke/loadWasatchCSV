import pandas as pd
import argparse
import os

# How to use:
# make sub-directory named data
# plase the CSV file in the directory
# run this script as
#  python load.py (name of CSV file).csv 
# if you add -or or -od, raw spectra or dark spectra corresponding to the spectrum is omitted, respectively

# In the measurement, NEVER forget to name each data as "sample_1_5s10a".
# Otherwise data load may cause some trouble.

if __name__ =="__main__":
     # parse options
    parser = argparse.ArgumentParser()
    parser.add_argument("-od","--OmitDark", help="select if to omit the dark spectrum for each data.",action ="store_true")
    parser.add_argument("-or","--OmitRaw", help="select if to omit the raw spectrum for each data.",action ="store_true")
    # for 1064 database use
    parser.add_argument("-ir","--IncRs", help="select if to include Raman shift column.",action ="store_true")
    parser.add_argument("path", type=str, help="write the full name of the CSV file")

    opt =parser.parse_args()

    addRs = opt.IncRs # whether to add rs column

    if(os.path.isfile(f"./data/{opt.path}") is False):
        print("*** No such CSV file in ./data/ directory. write the target CSV file name")
        sys.exit()
    else:
        print(f"*** data extraction on the file: {opt.path}")
    
    if(opt.OmitDark==True):
        print("**  Dark spectrum for each data will not be extracted")
    if(opt.OmitRaw==True):
        print("**  Raw spectrum for each data will not be extracted")
    
    os.makedirs(f"./data/{opt.path[:-4]}", exist_ok = True)
    df = pd.read_csv(f"./data/{opt.path}", header =None)
    df = df.iloc[34:,:].reset_index(drop=True)

    # raman shift
    print("**  =====")
    rs = df.iloc[1:,1]
    rs.to_csv(f"./data/{opt.path[:-4]}/rs.txt", index=False,header =False, sep='\t')
    print("*   Raman shift as rs.txt")
    
    for i in range(2,len(df.columns)): 
        if(i%3 ==2): # processed
            spc = df.iloc[0:,i]
            spc = spc.drop(spc.index[1])
            spc.to_csv(f"./data/{opt.path[:-4]}/{spc[0]}.txt", index=False,header=None, sep='\t')

            #2 column txt data
            if(addRs==True):
                tmpRs = rs.reset_index(drop=True)
                tmpSpc = spc.reset_index(drop=True)
                spcRs = pd.concat([tmpRs,tmpSpc],axis=1)
                spcRs.to_csv(f"./data/{opt.path[:-4]}/{spc[0]}_qc.txt", index=False,header=None, sep='\t')  

        elif(i%3 ==1): # dark
            if(opt.OmitDark ==True):
                continue

            spc = df.iloc[0:,i-2]
            spc = spc.drop(spc.index[1])
            spc.iloc[1:] = df.iloc[2:,i] 
            spc.iloc[0] = spc.iloc[0]+"_d"     
            spc.to_csv(f"./data/{opt.path[:-4]}/{spc[0]}.txt", index=False,header=None, sep='\t')

        elif(i%3 ==0): # raw data
            if(opt.OmitRaw ==True):
                continue

            spc = df.iloc[0:,i-1]
            spc = spc.drop(spc.index[1])
            spc.iloc[1:] = df.iloc[2:,i]    
            spc.iloc[0] = spc.iloc[0]+"_r"    
            spc.to_csv(f"./data/{opt.path[:-4]}/{spc[0]}.txt", index=False,header=None, sep='\t')

        print(f"*   {spc[0]}.txt")

    print("**  =====")
    print("*** extraction completed")

print(spcRs)
