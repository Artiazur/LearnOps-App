# Utility script for generating the RSA key pair used by JWT authentication.
#
# The generated private key is used to sign tokens, while the corresponding
# public key is used to verify them. Keeping key generation separate from the
# authentication runtime prevents the application from generating new keys
# every time it starts.

from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


# Generate a 2048-bit RSA private key with the standard public exponent.
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Derive the public key from the generated private key.
public_key = private_key.public_key()


# Create the output directory if it does not already exist.
Path("keys").mkdir(exist_ok=True)


# Store the private key in PEM format for JWT signing.
with open("keys/private.pem", "wb") as file:
    file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )


# Store the public key in PEM format for JWT signature verification.
with open("keys/public.pem", "wb") as file:
    file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )


print("Keys generated successfully!")