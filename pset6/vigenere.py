import cs50
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: ./vigenere k")
        exit(1)
    
    if sys.argv[1].isalpha() == False:
        print("Usage: ./vigenere k")
        exit(1)
    
    print("plaintext: ",end='')   
    message = cs50.get_string()
    translated = []
    keyIdx = 0
    keylen = len(sys.argv[1])
    
    for symbol in message:
        if symbol.isalpha():
            key = ord(sys.argv[1][keyIdx % keylen].lower()) - 97
            keyIdx += 1
            translated.append(caesar(symbol, key))
        else:
            translated.append(symbol)
    print("ciphertext: ",end='');
    print("".join(translated))
    exit(0)
    
def caesar(char, key):
    if char.isupper():
        return chr(((ord(char) - 65 + key) % 26) + 65)
    else:
        return chr(((ord(char) - 97 + key) % 26) + 97)

if __name__ == "__main__":
    main()