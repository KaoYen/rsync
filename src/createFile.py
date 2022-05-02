if __name__ == "__main__":
    with open('destination.txt', 'wb') as f:
        for i in range(4096):
            f.write('0')