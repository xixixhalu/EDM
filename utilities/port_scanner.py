import subprocess
import sys

def checkPort(port):
    try:
        subprocess.check_output(['lsof','-i',':'+str(port)])
        output = 0
    except:
        output = 1
    return output

def runPortScan(rangeLow, RangeHigh):
    availablePort = -1
    for port in range(rangeLow,RangeHigh+1):
        if checkPort(port) == 1:
            availablePort = port
            break
        else:
            continue
    if availablePort is not -1:
        return availablePort
    else:
        return "no ports available"

if len(sys.argv) == 3:
    # NITIN : NOTE : Vinita, if using through cmdline pass portHigh and portLow (inclusive) as
    # cmdline args to the script
    result = runPortScan(int(sys.argv[1]), int(sys.argv[2]))
else:
    # NITIN : NOTE : Vinita remove below line and pass port ranges(inclusive) as arguments to
    # runPortScan() function, it will return the first available port in the range,
    # typically we should always specify same range
    pass

# print result

