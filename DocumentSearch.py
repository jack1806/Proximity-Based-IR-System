import os


class DocumentSearch:

    def __init__(self) -> None:
        self.FILE_NAME_LOCATION = "TotalFiles.txt"
        super().__init__()

    def search(self):
        currentdir = os.getcwd()
        text = ""
        ret = []
        for r, d, f in os.walk(currentdir):
            for file in f:
                if ".pdf" in file:
                    text += os.path.join(r, file)+"\n"
                    ret.append(os.path.join(r, file))
        file = open(str(os.getcwd())+"/"+self.FILE_NAME_LOCATION, 'w')
        file.write(text)
        file.close()
        return ret
