import sys, getopt
opts, args = getopt.getopt(sys.argv[1:], "h")
def useage():
    for op, value in opts:
        if op == "-h":
            print('house.py cityname districtname')
            sys.exit()
useage()        