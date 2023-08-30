import re
from pydantic import BaseModel, Field, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from fastapi import HTTPException


class UserLogin(BaseModel):
    email: EmailStr = Field(
        title="email",
        alias="email",
        placeholder="example@parstasmim.com",
        description="Email address of user",
        minLength=8,
        maxLength=32,
        dataType="string",
        type="email",
        isRquired=True,
        regexPattern=r"^(?=.{1,256})(?=.{1,64}@.{1,255}$)(?=.{1,256}@.{1,256}$)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$",
    )
    password: str = Field(
        title="password",
        alias="password",
        placeholder="qwer1234QWER",
        description="8 characters at least",
        minLength=8,
        maxLength=32,
        dataType="string",
        type="password",
        isRquired=True,
        regexPattern=r"^[a-z]{1,29}$",
    )

    @field_validator("email")
    def validate_password(cls, email):
        pattern = r"^(?=.{1,256})(?=.{1,64}@.{1,255}$)(?=.{1,256}@.{1,256}$)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
        match = re.fullmatch(pattern, email)
        if not match:
            raise HTTPException(
                status_code=422,
                detail={"error": {"email": "Please enter a valid Email address"}},
            )
        return email

    @field_validator("password")
    def validate_password(cls, verify_password: str):
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"
        )
        match = re.fullmatch(pattern, verify_password)
        if not match:
            raise HTTPException(
                status_code=422,
                detail={"error": {"password": "Please enter a valid password"}},
            )
        return verify_password


class UserCreate(UserLogin):
    verify_password: str = Field(
        title="verify_password",
        alias="verifyPassword",
        placeholder="qwer1234QWER",
        description="8 characters at least",
        minLength=8,
        maxLength=32,
        dataType="string",
        type="password",
        isRquired=True,
        regexPattern=r"^([a-zA-Z0-9'!#$%&'*+/=?^_`{|}~.-]{6,32})",
    )

    @field_validator("verify_password")
    def validate_verify_password(cls, verify_password: str, info: FieldValidationInfo):
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"
        )
        match = re.fullmatch(pattern, verify_password)
        if not match:
            raise HTTPException(
                status_code=422,
                detail={"error": {"password": "Please enter a valid password"}},
            )
        if verify_password != info.data["password"]:
            raise HTTPException(
                status_code=422,
                detail={"error": {"verify_password": "Passwords do not match"}},
            )
        return verify_password


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True
