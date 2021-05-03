from tqdm import tqdm, trange
from random import random, randint
import time

# https://github.com/tqdm/tqdm


for i in tqdm(range(10)):
    time.sleep(0.01)


# trange(N) can be also used as a convenient shortcut for tqdm(range(N))

with trange(10) as t:
    for i in t:
        # Description will be displayed on the left
        t.set_description('GEN %i' % i)
        # Postfix will be displayed on the right,
        # formatted automatically based on argument's datatype
        t.set_postfix(loss=random(), gen=randint(1,999), str='h',
                      lst=[1, 2])
        time.sleep(0.1)


text = ""
for char in tqdm(["a", "b", "c", "d"]):
    time.sleep(0.25)
    text = text + char

pbar = tqdm(["pre", "installation", "post", "done"])
for char in pbar:
    pbar.set_description("doing %s" % char)
    time.sleep(1.25)

with tqdm(total=100) as pbar:
    for i in range(10):
        time.sleep(0.1)
        pbar.update(10)


# It can also be executed as a module with pipes:
# $ seq 9999999 | tqdm --bytes | wc -l