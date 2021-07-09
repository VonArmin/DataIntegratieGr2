import sys

pathin=str(sys.argv[1])
pathout=str(sys.argv[2])
data=[]

def main():
    openFiles()

def openFiles():
    file=open(pathin,'r')
    outfile=open(pathout,'w')
    written=0

    outfile.write("#CHROM,POS,ID,REF,ALT,QUAL,FILTER,INFO,FORMAT,PGPC_0002,2:PGPC_0002\n")

    for line in file:
        if not line.startswith('#'):
            line.replace('\t',',')
            if written<10:
                outfile.write(line)
                written+=1
    file.close()
    outfile.close()

main()
