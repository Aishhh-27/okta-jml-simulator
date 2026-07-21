from jwcrypto import jwk
import json

key = jwk.JWK.from_pem(
    open("secrets/okta_public.pem", "rb").read()
)

public_jwk = json.loads(key.export_public())

public_jwk["kid"] = "okta-jml-key-2026"
public_jwk["use"] = "sig"

print(json.dumps(public_jwk, indent=2))
