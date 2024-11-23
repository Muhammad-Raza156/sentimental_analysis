from pydantic import BaseModel, conlist
class ProductReviews(BaseModel):
    reviews: conlist(str, min_length=1) # type: ignore