import sys
import os

user = "mattis"

os.system("git pull origin main")
os.system("git checkout -b "+user)
os.system("git add .")
print("You are now on branch "+user)