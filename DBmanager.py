import typer
import DBsystem

app = typer.Typer()

@app.command()  # hello関数をhelloコマンドとして登録
def hello(name: str):
    typer.echo(f"Hello {name}!")

@app.command("bye")  # goodbye関数をbyeコマンドとして登録
def goodbye(name: str):
    typer.echo(f"Bye {name}!")

@app.command("main")
def show_main_db_with_target():
    typer.echo(f"main show df mode")
    while True:
        target = input('target name: ')

        if target == "bye":
            print('see you later :)')
        
        print(f'show {target} from main DB')
        DBsystem.show_main_info(target)

if __name__ == "__main__":
    app()