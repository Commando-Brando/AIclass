from queue import PriorityQueue

pq = PriorityQueue()

pq.put((0, "SA", ["SA"]))
stuff = pq.get()
print(stuff)
pq.put((0, "HT", stuff[2].append("HT")))
ht = pq.get()
print(ht)