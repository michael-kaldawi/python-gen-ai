class ArraysAndStrings:
    
    def isPalPermTest(self):
        sPalPerm = "hellooh" # holeloh
        sNotPalPerm = "welcome"
        assert self.isPalPerm(sPalPerm), "expect to pass test"
        assert not self.isPalPerm(sNotPalPerm), "expect to fail test"

    def isPalPerm(self, s):
        isPalPerm = False
        countOdd = 0
        dict = self.stringToDict(s)
        for item in dict.values():
            if item % 2 != 0:
                countOdd += 1
        
        if countOdd == 0 or countOdd == 1:
            isPalPerm = True
        return isPalPerm

    def URLifyTest(self):
        s = "Mr. John Doe"
        sExpected = "Mr.%20John%20Doe"
        assert self.URLify(s) == sExpected

    def URLify(self, s):
        return s.replace(" ", "%20")

    def isPermTest(self):
        s = "hello world"
        sPerm = "olleh orlwd"
        sNotPerm = "hello world:)"

        assert self.isPerm(s, sPerm), "expect to pass"
        assert not self.isPerm(s, sNotPerm), "expect to fail"

    def isPerm(self, s, s2):
        dict = self.stringToDict(s)
        dict2 = self.stringToDict(s2)

        for k, v in dict.items():
            if k in dict2 and dict2[k] == v:
                continue
            else:
                return False
        
        for k, v in dict2.items():
            if k in dict and dict[k] == v:
                continue
            else:
                return False

        return True

    def stringToDict(self, s):
        dict = {}
        for char in s:
            if char in dict:
                dict[char] +=1
            else:
                dict[char] = 1
        return dict

    def hasUniqueChars(self, s):
        for char in s:
            # search the string for the character starting
            # from the position after the index of char 
            if s[s.index(char)+1::].find(char) >= 0:
                return False
        return True

    def hasUniqueCharsTest(self):
        s = "supercali"
        s2 = "supercalifornia"

        assert self.hasUniqueChars(s), "expect to pass"
        assert not self.hasUniqueChars(s2), "expect to fail"