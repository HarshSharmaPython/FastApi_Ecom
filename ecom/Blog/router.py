from fastapi import APIRouter, HTTPException, status, Query
from ..models import CreateBlogs, Blog, BlogStatusEum, UpdateBlogType
from beanie import PydanticObjectId
from datetime import datetime,timezone
from beanie.operators import In

BlogRouter = APIRouter(tags=["Blog"])

@BlogRouter.post("/")
async def write_blogs(blog:CreateBlogs):
    slug = await Blog.find(Blog.slug==blog.slug).to_list()
    if len(slug) >0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Blog with this slug already")
    to_inssert_blog=Blog(**blog.model_dump())
    await to_inssert_blog.insert()
    return to_inssert_blog

@BlogRouter.get("/allblogs")
async def get_all_blogs(status: list[BlogStatusEum] = Query(None)):
    if status is None:
        blogs = await Blog.find_many().to_list()
    else:
        blogs = await Blog.find_many(In(Blog.status, status)).to_list()
    return blogs

@BlogRouter.get("/")
async def get_blog(blog_id: str):
    blog = None
    try:
        blog_id = PydanticObjectId(blog_id)
        blog = await Blog.get(blog_id)
    except Exception :
        blog = await Blog.find_one(Blog.slug==blog_id)
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

@BlogRouter.put("/")
async def update_blogs(blog_id:PydanticObjectId, update_details:UpdateBlogType):
    to_update=await Blog.get(blog_id)
    if not to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if update_details.slug!=to_update.slug:
        slug__exists = await Blog.find(Blog.slug==update_details.slug).to_list()
        if len(slug__exists)>0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Blog with this slug already")
    await to_update.set({**update_details.model_dump(exclude_none = True),"updated_at":datetime.now(timezone.utc)})
    return to_update


@BlogRouter.delete("/")
async def delete_blogs(blog_id:PydanticObjectId):
    blogs=await Blog.get(blog_id)
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    await blogs.delete()
    return {"Message":"Blog is Deleted Successfully"}
