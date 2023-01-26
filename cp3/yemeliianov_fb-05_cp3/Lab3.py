from class3 import Class_for_Bigram
def main():
    a=Class_for_Bigram()
    possibleKeys = a.find_possible_keys(a.bigrams_comparison(a.find_frequent_bigrams(a.clearString)))
    a.correct_keys(possibleKeys, a.clearString)
if __name__ == '__main__':
    main()