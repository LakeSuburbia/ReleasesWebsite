import sys
import os

if len(sys.argv) < 2:
    print("You should add a message!")
else:
    message="\""
    for i  in range(1,len(sys.argv)):
        message = message + sys.argv[i] + " "
    message=message+"\""
    
    os.system("git checkout sander")
    os.system("git add .")
    os.system('git commit -m '+message)
    print("Committed with message:")
    print(message)