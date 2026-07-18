FROM futureys/claude-code-python-development:20260710125000
COPY pyproject.toml uv.lock /workspace/
RUN uv sync
COPY . /workspace/
ENTRYPOINT ["uv", "run"]
CMD ["back_up.py"]
