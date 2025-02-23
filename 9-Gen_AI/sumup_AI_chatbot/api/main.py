import os
import sys

sys.path.append(os.path.abspath(".."))
# needs uvicorn installed: pip install uvicorn
from chain import sumup
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


# defining the URL tail, here it is just "/"
@app.get("/")
# function to run when "getting" that tail:
async def root():
    print("Hello World")


# ======= Run the API pointer =====
# 1. in the CLI: go to the folder where this main.py file is located
# 2. uvicorn main:app --reload
# 3. then CTRL click on the given local URL


# === making the API pointer for the sumup() function: ===
# defining the URL tail: /sum_up, on a POST protocol
@app.post("/sum_up")
async def sum_up(input_file: UploadFile = File(...)):
    # checking if the file is a .txt file, and if not, returning error:
    if input_file.content_type != "text/plain":
        return {"error": "Only text files are supported."}

    # leaves the text available:
    content = await input_file.read()
    # encoding the content to standard utf-8:
    text = content.decode("utf-8")
    # summarizing it:
    summary = sumup(text)

    return {"Summary": summary}


# ======= Use Swagger to try API =====
# once the app is ran, add to the URL: /docs to launch Swagger
# try out the sum_up function: upload the .txt file
