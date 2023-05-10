#Author: Jonathan Smith
#Date: 2023-04-20
#Description: This is the main file for the copilot test builder. It will be used to create the test cases for the project.

import pathlib
import random

class Typo:

    def __init__(self):
        pass

    def transpose(x : str):
        if len(x) > 1:
            i = random.randint(0, len(x)-2)
            y = x[:i] + x[i+1] + x[i] + x[i+2:]
            return y
        else:
            return ""

    def delete(x : str):
        if len(x) > 1:
            i = random.randint(0, len(x)-1)
            y = x[:i] + x[i+1:]
            return y
        else:
            return ""

    def replace(x : str):
        if len(x) > 0:
            i = random.randint(0, len(x)-1)
            l = 'abcdefghijklmnopqrstuvwxyz'
            u = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if x[i] in l:
                return x.replace(x[i], random.choice(l), 1)
            elif x[i] in u:
                return x.replace(x[i], random.choice(u), 1)
            else:
                return x
        else:
            return ""
        
    def insert(x : str):
        set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if len(x) > 0:
            i = random.randint(0, len(x)-1)
            y = x[:i] + random.choice(set) + x[i:]
        else:
            y = random.choice(set)
        return y

    def generate(x : str, chance : float, max : int):
        words = x.split(" ")
        newwords = []
        for word in words:
            newline = False
            if word.__contains__("\n"):
                newline = True
                word = word.replace("\n", "")
            for i in range(0, max):
                if random.random() <= chance:
                    operation = random.choice([Typo.transpose, Typo.delete, Typo.replace, Typo.insert])
                    word = operation(word)
            if newline:
                word += "\n"
            newwords.append(word)
        if len(newwords) > 0:
            return ' '.join(newwords)
        else:
            return x


class Prompt:

    promptname = ""
    description = ""
    requiredfunction = ""
    functionname = ""
    args = ""
    tc1 = ""
    tc2 = ""
    tc3 = ""
    lines = []
    test = None

    def __init__(self, lines : list):
        self.promptname = lines[0]
        self.description = lines[1]
        self.functionname = lines[2]
        self.args = lines[3]
        self.requiredfunction = lines[4]
        self.tc1 = lines[5]
        self.tc2 = lines[6]
        self.tc3 = lines[7]
        self.lines = lines.copy()

    def copy(self):
        return Prompt(self.lines)
    
    def __str__(self):
        return '\n'.join(self.lines)
    
    def applyTest(self):
        for key in self.test.flags.keys():
            if self.test.flags[key]:
                Test.applyTest[key](self)
    
    def promptToPython(self):
        result = ""
        #result += "# " + self.promptname + "\n"
        result += "# " + self.description + "\n"
        result += "def " + self.functionname + "(" + self.args + "):\n"
        result += "\n\n"
        if self.requiredfunction != "":
            result += self.requiredfunction + "\n"
        result += "def main():\n    " + self.tc1 + "\n    " + self.tc2 + "\n    " + self.tc3 + "\n"
        result += 'if __name__ == "__main__":\n    main()\n'
        return result

    
class Test:

    flags = {}
    name = ""

    def __init__(self, name : str, flags : str):
        self.flags = {"2":False,"3":False,"C":False,"D":False,"F":False,"H":False,"L":False,"M":False}
        self.assignFlags(flags)
        self.name = name

    def copy(self):
        return Test(self.name, self.getFlags())

    def assignFlags(self, flags : str):
        for flag in flags:
            self.flags[flag] = True

    def getFlags(self):
        x = [key for key, y in self.flags.items() if y == True]
        return ''.join(x)
    
    def test2(prompt : Prompt):
        prompt.tc2 = ""
        prompt.tc3 = ""
    
    def test3(prompt : Prompt):
        prompt.tc1 = ""
        prompt.tc2 = ""
        prompt.tc3 = ""

    def testControl(prompt : Prompt):
        pass
    
    def testNoDesc(prompt : Prompt):
        prompt.description = ""

    def testNoFunc(prompt : Prompt):
        prompt.tc1 = prompt.tc1.replace(prompt.functionname, "dummy")
        prompt.tc2 = prompt.tc2.replace(prompt.functionname, "dummy")
        prompt.tc3 = prompt.tc3.replace(prompt.functionname, "dummy")
        prompt.functionname = "dummy"

    def testL(prompt : Prompt):
        desc = Typo.generate(prompt.description, 0.05, 2)
        prompt.description = desc

    def testM(prompt : Prompt):
        desc = Typo.generate(prompt.description, 0.05, 5)
        prompt.description = desc

    def testH(prompt : Prompt):
        desc = Typo.generate(prompt.description, 0.05, 12)
        prompt.description = desc

    applyTest = {"2":test2,"3":test3,"C":testControl,"D":testNoDesc,"F":testNoFunc,"H":testH,"L":testL,"M":testM}

class PromptBuilder:

    mainpath = pathlib.Path.cwd()
    promptlist = []
    promptarray = []
    tests = []
    numtests = 0
    uniqueprompts = 0

    def __init__(self):
        pass

    def run(self):
        self.openPromptFile()
        self.openTestsFile()
        for prompt in self.promptlist:
            promptclones = []
            for i in range(0, self.numtests):
                promptclones.append(prompt.copy())
            self.promptarray.append(promptclones)
        self.uniqueprompts = self.promptarray.__len__()
        self.setPromptTests()
        self.applyTeststoPrompts()
        self.writeOutputFiles()

    def openPromptFile(self):
        promptfile = pathlib.Path.open(self.mainpath.__str__() + "\prompts.txt", "r")
        prompts = promptfile.read().split("prompt name:")
        promptfile.close()
        prompts.pop(0)
        for prompt in prompts:
            splitvalues = ["description:", "function name:", "args:", "required function:", "tc1:", "tc2:", "tc3:"]
            promptvalues = []
            for splitvalue in splitvalues:
                x = prompt.split(splitvalue, 1)
                promptvalues.append(x[0].strip())
                prompt = x[1].strip()
            promptvalues.append(prompt)
            newprompt = Prompt(promptvalues)
            self.promptlist.append(newprompt)
    
    def openTestsFile(self):
        testsfile = pathlib.Path.open(self.mainpath.__str__() + "/tests.txt", "r")
        tests : list = testsfile.read().split("\n")
        self.numtests = tests.__len__()
        testsfile.close()
        for test in tests:
            x = test.split(":", 1)
            newtest = Test(x[0], x[1])
            self.tests.append(newtest)
    
    def setPromptTests(self):
        for i in range(0, self.uniqueprompts):
            for j in range(0, self.numtests):
                self.promptarray[i][j].test = self.tests[j].copy()
    
    def applyTeststoPrompts(self):
        for prompts in self.promptarray:
            for prompt in prompts:
                prompt.applyTest()
    
    def writeOutputFiles(self):
        for i in range(0, self.uniqueprompts):
            for j in range(0, self.numtests):
                fileid = str(i) + "-" + self.promptarray[i][j].test.getFlags()
                pathlib.Path(self.mainpath.__str__() + "\\output\\" + fileid).mkdir(parents=True, exist_ok=True)
                outputfile = pathlib.Path.open(self.mainpath.__str__() + "\\output\\" + fileid + "\\output.py", "w")
                outputfile.write(self.promptarray[i][j].promptToPython())
                outputfile.close()
            
        # print(prompts)


def main():
    random.seed(1)
    parser = PromptBuilder()
    parser.run()

if __name__ == "__main__":
    main()