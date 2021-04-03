import sys
import os

user = "sander"

os.system("git pull")
os.system("git checkout -b "+user)
os.system("git add .")
print("You are now on branch "+user)