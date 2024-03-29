from lab2.sjp.dictionary import Dictionary
import matplotlib.pyplot as plt
import json
import math
from scipy.optimize import curve_fit
from lab2.wordngrams import WordNGrams


def main():
    hw4(50)


def hw4(n=None):
    with open('./examples/potop.txt', encoding='UTF-8') as file:
        ngrams_2 = WordNGrams(2)
        ngrams_3 = WordNGrams(3)

        for line in file:
            ngrams_2.apply_text(line)
            ngrams_3.apply_text(line)

        print_n_grams(ngrams_2, n)
        print_n_grams(ngrams_3, n)


def print_n_grams(ngrams, n=None):
    data = sorted(ngrams.map.items(), key=lambda kv: (kv[1], kv[0]))[::-1]

    n = len(data) if n is None else n
    x = [x for x, y in data][:n]
    y = [y for x, y in data][:n]

    print(x)

    plt.plot(y, 'ro')
    plt.xticks(range(n), x, rotation=90)
    plt.show()


def hw3():
    with open('./cache/potop.basics.cache.json') as file:
        data = json.load(file)
        data = sorted(data.items(), key=lambda kv: (kv[1], kv[0]))[::-1]

        length = 0
        hl = 0
        for word, count in data:
            if count == 1:
                hl += 1

            length += count

        half = length / 2
        size = 0
        for word, count in data:
            half -= count
            size += 1

            if half <= 0:
                break

        print('basic words in text:', len(data))
        print('hapax legomena:', hl)
        print('50% of text consist of:', size, 'words')


def hw2(n=None):
    with open('./cache/potop.basics.cache.json') as file:
        data = json.load(file)
        data = sorted(data.items(), key=lambda kv: (kv[1], kv[0]))[::-1]

        n = len(data) if n is None else n
        y = [y for x, y in data][:n]

        plt.plot(y, 'g')

        # zipf
        k = 27157.65
        z = [k / x if x != 0 else math.inf for x in range(n)]
        plt.plot(z, 'r', label='zipf')

        # mandelbrot
        P = 34618.562
        B = 0.981068
        d = 0.432793
        m = [P / ((x + d) ** B) if x != 0 else math.inf for x in range(n)]
        plt.plot(m, 'b', label='mandelbrot')

        plt.legend()
        plt.show()


def get_params():
    with open('./cache/potop.basics.cache.json') as file:
        data = json.load(file)
        data = sorted(data.items(), key=lambda kv: (kv[1], kv[0]))[::-1]

        x = [i + 1 for i in range(len(data))]
        y = [y for x, y in data]

        print(curve_fit(zipf, x, y))
        print(curve_fit(mandelbrot, x, y))


def zipf(x, k):
    return k / x


def mandelbrot(x, P, B, d):
    return P / ((x + d) ** B)


def hw1(n=None):
    with open('./cache/potop.basics.cache.json') as file:
        data = json.load(file)
        data = sorted(data.items(), key=lambda kv: (kv[1], kv[0]))[::-1]

        n = len(data) if n is None else n
        y = [y for x, y in data][:n]
        plt.plot(y, 'ro')
        plt.show()


def create_basics_cache():
    with open('./cache/potop.cache.json', 'r') as file:
        potop = json.load(file)

    basics = {}
    dic = Dictionary()
    for word, count in potop.items():
        basic = dic.get_basic_form(word)

        if basic is None:
            continue

        basics[basic] = (basics[basic] if basic in basics else 0) + count

    with open('./cache/potop.basics.cache.json', 'w') as file:
        json.dump(basics, file)


if __name__ == '__main__':
    main()
