from fastapi import FastAPI

screening_app = FastAPI()

@screening_app.get("/")
async def root():
    result = get_full_name("Harvy Jones", "Pontillas")
    return result

def get_full_name(fname: str, lname: str):
    full_name = fname.title() + " " + lname.title()
    return full_name