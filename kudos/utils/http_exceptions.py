from fastapi import HTTPException, status

def http_400(detail: str):
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

def http_401(detail: str = "Not authenticated"):
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

def http_403(detail: str = "Forbidden"):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

def http_404(detail: str):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

def http_500(detail: str = "Internal Server Error"):
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
