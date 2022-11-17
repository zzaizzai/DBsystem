import typer
import DBsystem
import SaveMainDB

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
@app.command("save")
def save_data_in_mainDB():
    typer.echo(f"save mode")
    while True:
        target = input('target name: ')

        if target == "bye":
            print('see you later :)')
        
        print(f'save {target} from data excel')
        SaveMainDB.read_new_df(target)
@app.command("compare")
def compare_data_in_mainDB():
    target_list = []
    while True:

        print('current target list: ',target_list)
        a = input(f'target_list: ')
        if a == 'go':
            break
        elif a== 'remove':
            target_list.pop()
        else:
            target_list.append(a)

    DBsystem.show_main_info_compare(target_list)


if __name__ == "__main__":
    app()