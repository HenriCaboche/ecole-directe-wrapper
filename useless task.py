import random
import threading

letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," "]
target = "oh rage"
found = False
a = 0
len = len(list(target))
print(len)
lock = threading.Lock()

def guesser():
    global found, a
    while not found:
        guess = []
        for x in range(len):
            guess.append(letters[random.randint(0,25)])
        guess = "".join(guess)
        a+=1
        with lock:

            if guess == target:
                found = True

threads = []
for i in range(16):  
    t = threading.Thread(target=guesser)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
print( a)