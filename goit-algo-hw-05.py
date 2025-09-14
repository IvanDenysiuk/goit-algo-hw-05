import requests
import timeit
import pandas as pd

# Алгоритми

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    j = 0

    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps(pattern)
    i = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def bm_search(text, pattern):
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1

    skip = {}
    for k in range(m - 1):
        skip[pattern[k]] = m - k - 1
    k = m - 1

    while k < n:
        j = m - 1
        i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1
            i -= 1
        if j == -1:
            return i + 1
        k += skip.get(text[k], m)
    return -1


def rabin_karp(text, pattern, q=101):
    d = 256
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1
    p = 0
    t = 0
    h = 1
    for i in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return -1

# Завантаження файлів з Google Drive 

def download_from_drive(file_id, filename):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

# ID
id1 = "18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh"
id2 = "18BfXyQcmuinEI_8KDSnQm4bLx6yIFS_w"

download_from_drive(id1, "article1.txt")
download_from_drive(id2, "article2.txt")

with open("article1.txt", "r", encoding="utf-8", errors="ignore") as f:
    text1 = f.read()
with open("article2.txt", "r", encoding="utf-8", errors="ignore") as f:
    text2 = f.read()

# Підрядки

pattern_exist = " ".join(text1.split()[:5])   # перші 5 слів
pattern_fake = "qwerty12345"

# Вимір часу

def measure(text, pattern, func):
    return timeit.timeit(lambda: func(text, pattern), number=10)

algorithms = {
    "KMP": kmp_search,
    "Boyer-Moore": bm_search,
    "Rabin-Karp": rabin_karp
}

results = []

for text_name, text in [("Article 1", text1), ("Article 2", text2)]:
    for pattern_name, pattern in [("Existing", pattern_exist), ("Fake", pattern_fake)]:
        for algo_name, algo_func in algorithms.items():
            t = measure(text, pattern, algo_func)
            results.append((text_name, pattern_name, algo_name, t))

df = pd.DataFrame(results, columns=["Text", "Pattern", "Algorithm", "Time (s)"])
print("\n Результати вимірювань:")
print(df)

# Аналіз

summary = {}

for text in df["Text"].unique():
    df_text = df[df["Text"] == text]
    best = df_text.loc[df_text["Time (s)"].idxmin()]
    summary[text] = (best["Algorithm"], best["Time (s)"])

overall_best = df.loc[df["Time (s)"].idxmin()]

print("\n Найшвидші алгоритми:")
for text, (algo, t) in summary.items():
    print(f"- {text}: {algo} ({t:.6f} сек)")

print(f"- Загалом: {overall_best['Algorithm']} на {overall_best['Text']} ({overall_best['Time (s)']:.6f} сек)")
