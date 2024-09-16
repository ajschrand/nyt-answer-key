from json import load
    
class bitset:
    @staticmethod
    def get_bit(char):
        return 1 << (ord(char) - ord("a"))
    
    def __init__(self, word="", bits=0):
        self.bits = 0
        if word:
            for char in word:
                self.bits |= bitset.get_bit(char)
        elif bits:
            self.bits = bits
            
    def add(self, char):
        bit = bitset.get_bit(char)
        self.bits |= bit
        
    def remove(self, char):
        bit = bitset.get_bit(char)
        if self.bits & bit == 0:
            raise KeyError(char)
        
        self.bits ^= bit
        
    def discard(self, char):
        bit = bitset.get_bit(char)
        if self.bits & bit == 0:
            return
        
        self.bits ^= bit
        
    def clear(self):
        self.bits = 0
        
    def union(self, other):
        bits = self.bits | other.bits
        return bitset(bits=bits)
    
    def intersection(self, other):
        bits = self.bits & other.bits
        return bitset(bits=bits)
    
    def difference(self, other):
        bits = self.bits ^ (self.bits & other.bits)
        return bitset(bits=bits)
    
    def symmetric_difference(self, other):
        bits = self.bits ^ other.bits
        return bitset(bits=bits)
    
    def isdisjoint(self, other):
        return self.bits & other.bits == 0
    
    def issubset(self, other):
        return self.bits & other.bits == self.bits
    
    __add__ = union
    __sub__ = difference
    __and__ = intersection
    __xor__ = symmetric_difference
    __or__ = union
    
    def __eq__(self, other):
        return self.bits == other.bits
    
    def __hash__(self):
        return hash(self.bits)
    
    def __len__(self):
        return self.bits.bit_count()
    
    def __contains__(self, char):
        bit = bitset.get_bit(char)
        return self.bits & bit > 0
    
    def __iter__(self):
        self.index = 0
        self.cur = self.bits
        return self
    
    def __next__(self):
        while self.cur:
            if self.cur & (1 << self.index):
                char = chr(ord('a') + self.index)
                self.index += 1
                return char
            
            self.index += 1
            
        raise StopIteration

    def __str__(self):
        letters = ", ".join(letter for letter in self)
        return "{" + letters + "}"
            

def get_list_grid(list, size):
    grid = ""
    line = ""
    for i, word in enumerate(list):
        line += str(word) + " "
        if (i + 1) % size == 0:
            grid += line + "\n"
            line = ""

    return grid.strip()


def word_has_all(word, letters):
    return bitset(letters).issubset(bitset(word))


def word_has_only(word, letters):
    for letter in word:
        if letter not in letters:
            return False

    return True


def word_has_duplicates(word):
    seen = bitset()
    for letter in word:
        if letter in seen:
            return True
        
        seen.add(letter)

    return False


def get_english_words():
    return load(open(f"utils/english_words.txt", 'r'))


def get_wordle_answers():
    return load(open(f"utils/wordle_answers.txt", 'r'))

