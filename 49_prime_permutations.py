# -*- coding: utf-8 -*-
import math


def is_prime(n):
    sqrt_n = math.ceil(math.sqrt(n))
    for i in range(2, int(sqrt_n)):
        if n % i == 0:
            return False
    return True


def permute_list(perms, current, pending):
    if len(pending) == 1:
        current += pending
        num = int(''.join(current))
        perms.add(num)
    for i in range(0, len(pending)):
        new_selection = current + [pending[i]]
        new_left = pending[0:i] + pending[i + 1:]
        permute_list(perms, new_selection, new_left)


def find_ascending_seq(lst):
    for i in range(len(lst)):
        pair1 = lst[i]
        seq = [pair1[0], pair1[1]]
        curr = pair1[1]
        for j in range(i, len(lst)):
            pair2 = lst[j]
            if pair2[0] == curr:
                seq.append(pair2[1])
                curr = pair2[1]

        if len(seq) == 3:
            return seq


def find_prime_perms(n, has_computed_dict):
    digit_list = [i for i in str(n)]
    perms = set()
    permute_list(perms, [], digit_list)
    perms = sorted(perms)
    prime_perms = [n]
    for i in perms[perms.index(n) + 1:]:
        has_computed_dict[i] = True
        if is_prime(i):
            prime_perms.append(i)

    diff_list = []
    for i in range(len(prime_perms)):
        x = prime_perms[i]
        for j in range(i, len(prime_perms)):
            y = prime_perms[j]
            if y - x == 3330:
                diff_list.append((x, y))
    return find_ascending_seq(diff_list)


def main():
    has_computed = {}
    for i in range(1000, 10000):
        if i in has_computed:
            continue

        has_computed[i] = True
        if is_prime(i):
            prime_perms = find_prime_perms(i, has_computed)
            if prime_perms and len(prime_perms) == 3:
                if prime_perms[0] != 1487:
                    print("".join(map(lambda x: str(x), prime_perms)))


if __name__ == "__main__":
    main()
