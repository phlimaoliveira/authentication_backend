from ORM.TokenBlocklist import TokenBlocklist

class ManageTokenBlocklist:
    def new(jti, created_at):
        token = TokenBlocklist()
        token.jti = jti
        token.created_at = created_at
        token.save()

