class TextFile:
    def __init__(self, filename):
        self.filename = filename

        self.file = open(self.filename, "r")

        self.lines = []

        for line in self.file.readlines():
            if len(line) < 22:
                self.lines.append(line)
            else:
                self.lines.extend([line[i:i + 22] for i in range(0, len(line), 22)])


        print(self.lines)