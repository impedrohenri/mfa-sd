from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    RegisterRequest,
    VerifyRegisterRequest,
    LoginRequest,
    VerifyLoginRequest
)

from app.services.auth_service import (
    create_user,
    verify_user,
    authenticate_user,
    generate_token,
    fake_users
)

from app.services.mfa_service import (
    generate_code,
    verify_code
)

from app.utils.cryptography import (
    encrypt_email,
    decrypt_email
)

from app.utils.email import send_confirmation_email

router = APIRouter()



@router.post("/register")
async def register(data: RegisterRequest):

    user = create_user(data.email, data.password)

    if not user:
        raise HTTPException(400, "Usuário já existe")

    code = generate_code(data.email, "register")

    await send_confirmation_email(
        data.email,
        code,
        "Confirmação de Cadastro"
    )

    return {
        "message": "Código enviado no email"
    }


@router.post("/verify-register")
def verify_register(data: VerifyRegisterRequest):

    valid = verify_code(
        data.email,
        data.code,
        "register"
    )

    if not valid:
        raise HTTPException(401, "Código inválido")

    verify_user(data.email)

    return {
        "message": "Conta confirmada"
    }


@router.post("/login")
async def login(data: LoginRequest):

    valid = authenticate_user(
        data.email,
        data.password
    )

    if not valid:
        raise HTTPException(401, "Credenciais inválidas")

    code = generate_code(data.email, "login")

    await send_confirmation_email(
        data.email,
        code,
        "Código MFA Login"
    )

    return {
        "message": "Código MFA enviado"
    }


@router.post("/verify-login")
def verify_login(data: VerifyLoginRequest):

    valid = verify_code(
        data.email,
        data.code,
        "login"
    )

    if not valid:
        raise HTTPException(401, "Código inválido")

    token = generate_token()

    return {
        "message": "Login realizado",
        "token": token
    }

@router.get("/users")
def list_users():
    return fake_users



@router.get("/demo-encryption")
def demo_encryption():

    users = []

    for encrypted_email, user_data in fake_users.items():

        decrypted_email = decrypt_email(encrypted_email)

        users.append({
            "original_email": decrypted_email,
            "encrypted_email": encrypted_email,
            "password_hash": user_data["password"],
            "verified": user_data["verified"]
        })

    return {
        "total_users": len(users),
        "users": users
    }