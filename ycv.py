import typer
import yaml
from pygments import highlight
from pygments.lexers import YamlLexer
from pygments.formatters import Terminal256Formatter

app = typer.Typer()


def validate_yaml_file(file_path: str):
    with open(file_path) as file:
        try:
            yaml.safe_load(file)
            typer.secho(f"Validation successful: {file_path}", fg=typer.colors.GREEN)
        except yaml.YAMLError as e:
            typer.secho(f"Validation failed: {file_path}", fg=typer.colors.RED)
            if hasattr(e, "problem_mark"):
                mark = e.problem_mark
                typer.secho(
                    f"Error position: line {mark.line + 1}, column {mark.column + 1}",
                    fg=typer.colors.RED,
                )
            with open(file_path) as f:
                contents = f.read()
                formatted_yaml = highlight(
                    contents, YamlLexer(), Terminal256Formatter(style="monokai")
                )
                typer.echo(formatted_yaml, err=True)
                typer.echo(str(e), err=True)


@app.command()
def validate(file_path: str):
    """
    Validate a YAML file before deployment in Kubernetes
    """
    validate_yaml_file(file_path)


if __name__ == "__main__":
    app()
