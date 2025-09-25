WORKDIR/app
COPY requirements.txt/app/requirement.txt
RUN pip install --no-cache-dir-r/app/requirement.txt

COPY backend /app/backend
EVN PYTHONPARTH=/app
CMD["uvicormn","backend.app.main:app","--host","0.0.0","--port","8000"]
