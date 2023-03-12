

def killProcessRunningAtPort(port):
    import subprocess
    port=str(port)
    command="netstat -ano | findstr :"+port
    output=subprocess.getoutput(command).split('\n')
    PIDs=[]
    for i in output:
        if "127.0.0.1:"+port in i and "LISTENING" in i:
            PIDs.append(i.split()[-1])
    print("Processes with PIDs Running on Port",port,":",PIDs)
    for i in PIDs:
        print("Killing "+i)
        subprocess.getoutput("taskkill /PID "+i+" /F")
    print("Port "+port+" is free now!")

killProcessRunningAtPort(port=8080)
