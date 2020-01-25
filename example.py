
def gcd(a, b):
    if (a == 0) | (b == 0):
        return(a+b)
    else:
        return(gcd((max(a,b))%(min(a,b)), min(a,b)))


def main():
    a, b = map(int, input().split())
    print(gcd(a, b))


if __name__ == "__main__":
    main()