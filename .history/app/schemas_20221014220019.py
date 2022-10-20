

# ___this is our schema/pydantic model___
# it defines the structure of a request & response
# this insures the user will type exactly whats needed


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
# _____________________________________________
