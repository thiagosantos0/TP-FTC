import sys

def readFiles():
    arq = sys.argv[1]
    content = []
    with open(arq, 'r') as f:
        content = f.read().splitlines()
        print(content)
    return ""

readFiles()