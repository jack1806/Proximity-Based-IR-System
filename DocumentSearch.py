import os


class DocumentSearch:

    def __init__(self) -> None:
        super().__init__()

    def search(self):
        currentdir = os.getcwd()
        for r, d, f in os.walk(currentdir):
            for file in f:
                if ".pdf" in file:
                    print("file")
