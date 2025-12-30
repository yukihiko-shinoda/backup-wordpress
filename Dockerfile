FROM futureys/claude-code-python-development:latest
COPY pyproject.toml uv.lock /workspace/
RUN uv sync --python 3.13
COPY . /workspace/
ENTRYPOINT ["uv", "run"]
CMD ["back_up.py"]
