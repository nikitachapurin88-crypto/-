"""
Sorting algorithms.
Each function receives a list of ints and returns a list of step dicts:
  {
    "arr":  [...],   # full array state at this step
    "cmp":  [i, j],  # indices being compared  (or [])
    "swap": [i, j],  # indices just swapped     (or [])
    "done": [...]    # indices already in final position
  }
"""


def _snap(arr, steps, stats, cmp=None, swap=None, done=None):
    if cmp:
        stats["cmps"] += 1
    if swap:
        stats["swaps"] += 1
    steps.append({
        "arr":  list(arr),
        "cmp":  cmp  or [],
        "swap": swap or [],
        "done": list(done or []),
        "cmps": stats["cmps"],
        "swaps": stats["swaps"],
    })


# ── Bubble sort ──────────────────────────────────────────────────────────────

def bubble_sort(arr):
    a = list(arr)
    n = len(a)
    steps = []
    stats = {"cmps": 0, "swaps": 0}
    done = []

    for i in range(n - 1):
        for j in range(n - i - 1):
            _snap(a, steps, stats, cmp=[j, j + 1], done=done)
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                _snap(a, steps, stats, swap=[j, j + 1], done=done)
        done = [*done, n - 1 - i]

    _snap(a, steps, stats, done=list(range(n)))
    return steps


# ── Insertion sort ───────────────────────────────────────────────────────────

def insertion_sort(arr):
    a = list(arr)
    n = len(a)
    steps = []
    stats = {"cmps": 0, "swaps": 0}

    for i in range(1, n):
        j = i
        while j > 0:
            _snap(a, steps, stats, cmp=[j - 1, j])
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                _snap(a, steps, stats, swap=[j - 1, j])
                j -= 1
            else:
                break

    _snap(a, steps, stats, done=list(range(n)))
    return steps


# ── Selection sort ───────────────────────────────────────────────────────────

def selection_sort(arr):
    a = list(arr)
    n = len(a)
    steps = []
    stats = {"cmps": 0, "swaps": 0}
    done = []

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            _snap(a, steps, stats, cmp=[min_idx, j], done=done)
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            _snap(a, steps, stats, swap=[i, min_idx], done=done)
        done = [*done, i]

    _snap(a, steps, stats, done=list(range(n)))
    return steps


# ── Quick sort ───────────────────────────────────────────────────────────────

def quick_sort(arr):
    a = list(arr)
    steps = []
    stats = {"cmps": 0, "swaps": 0}

    def _qsort(lo, hi):
        if lo >= hi:
            return
        pivot = a[hi]
        p = lo
        for j in range(lo, hi):
            _snap(a, steps, stats, cmp=[j, hi])
            if a[j] <= pivot:
                a[p], a[j] = a[j], a[p]
                _snap(a, steps, stats, swap=[p, j])
                p += 1
        a[p], a[hi] = a[hi], a[p]
        _snap(a, steps, stats, swap=[p, hi])
        _qsort(lo, p - 1)
        _qsort(p + 1, hi)

    _qsort(0, len(a) - 1)
    _snap(a, steps, stats, done=list(range(len(a))))
    return steps


# ── Merge sort ───────────────────────────────────────────────────────────────

def merge_sort(arr):
    a = list(arr)
    steps = []
    stats = {"cmps": 0, "swaps": 0}

    def _msort(lo, hi):
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        _msort(lo, mid)
        _msort(mid + 1, hi)

        left  = a[lo:mid + 1]
        right = a[mid + 1:hi + 1]
        i = j = 0
        k = lo

        while i < len(left) and j < len(right):
            _snap(a, steps, stats, cmp=[lo + i, mid + 1 + j])
            if left[i] <= right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            _snap(a, steps, stats, swap=[k])
            k += 1

        while i < len(left):
            a[k] = left[i]
            _snap(a, steps, stats, swap=[k])
            i += 1
            k += 1

        while j < len(right):
            a[k] = right[j]
            _snap(a, steps, stats, swap=[k])
            j += 1
            k += 1

    _msort(0, len(a) - 1)
    _snap(a, steps, stats, done=list(range(len(a))))
    return steps


# ── Shell sort ───────────────────────────────────────────────────────────────

def shell_sort(arr):
    a = list(arr)
    n = len(a)
    steps = []
    stats = {"cmps": 0, "swaps": 0}
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            j = i
            while j >= gap:
                _snap(a, steps, stats, cmp=[j - gap, j])
                if a[j - gap] > a[j]:
                    a[j - gap], a[j] = a[j], a[j - gap]
                    _snap(a, steps, stats, swap=[j - gap, j])
                    j -= gap
                else:
                    break
        gap //= 2

    _snap(a, steps, stats, done=list(range(n)))
    return steps


# ── Registry ─────────────────────────────────────────────────────────────────

ALGORITHMS = {
    "bubble":    bubble_sort,
    "insertion": insertion_sort,
    "selection": selection_sort,
    "quick":     quick_sort,
    "merge":     merge_sort,
    "shell":     shell_sort,
}


def get_steps(arr: list, algorithm: str) -> list:
    fn = ALGORITHMS.get(algorithm)
    if fn is None:
        raise ValueError(f"Unknown algorithm: {algorithm!r}")
    return fn(arr)
