from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import *
from schemas import *
from database import engine

from passlib.context import CryptContext

from jose import jwt, JWTError

from datetime import datetime, timedelta

from fastapi.security import HTTPBearer


# ---------------- APP ----------------

app = FastAPI()

security = HTTPBearer()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# ---------------- DATABASE ----------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ---------------- JWT CONFIG ----------------

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ---------------- HASH PASSWORD ----------------

def hash_password(password: str):

    return pwd_context.hash(password)


# ---------------- VERIFY PASSWORD ----------------

def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ---------------- CREATE TOKEN ----------------

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ---------------- GET CURRENT USER ----------------

def get_current_user(

    token = Depends(security),

    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token"
    )

    try:

        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:

        raise credentials_exception

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise credentials_exception

    return user


# ---------------- PAGES ----------------

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signin.html",
        context={}
    )


@app.get("/signin")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signin.html",
        context={}
    )


@app.get("/signup")
def signup_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={}
    )


@app.get("/taskmanager")
def taskmanager(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ---------------- SIGNUP ----------------

@app.post("/signup")
def signup(

    user: UserCreate,

    db: Session = Depends(get_db)
):

    old_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if old_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(

        username=user.username,

        email=user.email,

        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    return {
        "message": "Signup successful"
    }


# ---------------- LOGIN ----------------

@app.post("/signin")
def signin(

    user: UserLogin,

    db: Session = Depends(get_db)
):

    old_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not old_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        user.password,
        old_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    token = create_access_token(
        {"sub": str(old_user.id)}
    )

    return {

        "message": "Login successful",

        "access_token": token
    }


# ---------------- ADD TASK ----------------

@app.post("/addtask")
def add_task(

    task: Taskcreate,

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)
):

    new_task = Task(

        title=task.title,

        note=task.note,

        status=task.status,

        user_id=current_user.id
    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return {

        "message": "Task added",

        "task": new_task
    }


# ---------------- GET TASKS ----------------

@app.get("/tasks")
def tasks(

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)
):

    return db.query(Task).filter(
        Task.user_id == current_user.id
    ).all()


# ---------------- UPDATE TASK ----------------

@app.put("/tasks/{id}")
def updatetask(

    id: int,

    task: Taskcreate,

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)
):

    old_task = db.query(Task).filter(
        Task.id == id,
        Task.user_id == current_user.id
    ).first()

    if not old_task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    old_task.title = task.title

    old_task.note = task.note

    old_task.status = task.status

    db.commit()

    return {
        "message": "Task updated"
    }


# ---------------- DELETE TASK ----------------

@app.delete("/tasks/{id}")
def deletetask(

    id: int,

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == id,
        Task.user_id == current_user.id
    ).first()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)

    db.commit()

    return {
        "message": "Deleted"
    }