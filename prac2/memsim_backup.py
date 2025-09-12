#!/usr/bin/env python3

import sys

def main():
    # define  physical frames in memory 
    frames = 3
    # Replacement policy 
    policy = "FIFO"
    pages = []

    # Read trace 
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("#"):  # skip blanks and comments
            continue
        pages.append(int(line))

    # Initialize memory and counters
    memory = []
    hits, misses, evictions = 0, 0, 0

    # Process each page
    for p in pages:
        if p in memory:
            # Page already in memory:Its a hit
            hits += 1
        else:
            # Page not in memory → Its a miss
            misses += 1
            if len(memory) < frames:
                # Free slot available 
                memory.append(p)
            else:
                # FIFO replacement
                memory.pop(0)
                evictions+=1
                memory.append(p)
               

    print("=== memsim results ===")
    print(f"policy:     {policy}")
    print(f"frames:     {frames}")
    print(f"references: {len(pages)}")
    print(f"hits:       {hits}")
    print(f"misses:     {misses}")
    print(f"evictions:  {evictions}")
    print(f"hit_rate:   {hits/len(pages):.2%}")

if __name__ == "__main__":
    main()

