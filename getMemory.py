import os
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])
def main():
    memory=getDiskSpace()
    memory=memory[3].split("%")[0]
    if int(memory) >= 9:
        os.system('cd mp4Video/')
        all_video=os.popen(['ls']) 
        print(all_video[0])   
main()

