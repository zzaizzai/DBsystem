import pandas as pd
import os
import re
import click

path_DB_main = os.path.expanduser('~/Desktop') + '/DBsystem/DB_main.xlsx'
path_method = os.path.expanduser('~/Desktop') + '/DBsystem/DB_method.xlsx'
path_target = os.path.expanduser('~/Desktop') + '/DBsystem/DB_target.xlsx'

# df_main = pd.read_excel(path_DB_main, sheet_name='DB', index_col=None)
df_method = pd.read_excel(path_method, sheet_name='method', index_col=None)
df_target = pd.read_excel(path_target, sheet_name='target', index_col=None)

# print(df_main)
print(df_method)


def read_new_df(target: str):
    path_new = os.path.expanduser(
        '~/Desktop') + f'/{target} Data/{target} Data.xlsx'
    df_new = pd.read_excel(path_new, sheet_name='Sheet1', index_col=0)
    df_new = df_new.reset_index(drop=True)
    # print(df_new.columns.to_list()[4:])
    target_list: list[str] = df_new.columns.to_list()[4:]

    def reference_method_table_to_get_method_id(a):
        if a == "" or a == None:
            return 89

        a_first_name = re.split('[_ ]', a)[0]
        # print(len(df_method[df_method["method_name"].str.contains(a_first_name)]["id"]))
        if len(df_method[df_method["method_name"].str.contains(a_first_name)]["id"]) > 0:
            id_method = df_method[df_method["method_name"].str.contains(
                a_first_name)]["id"].to_list()[0]
            return id_method
        else:
            return 99

    for a_target in target_list:

        df_main = pd.read_excel(path_DB_main, sheet_name='DB', index_col=None)
        df_main = df_main.reset_index(drop=True)
        # print(a_target)
        df_new_temp = df_new
        df_new_temp["value"] = df_new_temp[a_target]
        df_new_temp["target"] = a_target
        df_new_temp["method_id"] = df_new_temp["method"].apply(
            reference_method_table_to_get_method_id)
        # print(df_new_temp.loc[:, ["target" ,'method', 'condition', 'type', 'unit', "value"]])
        # print(df_new_temp)
        df_new_merge = df_new_temp.loc[:, [
            "target", 'method_id', 'condition', 'type', 'unit', "value"]]
        # print(df_new_merge.to_markdown())

        def update_row_data(df_old, df_object_new: object):

            if df_object_new.dtypes != object:
                return

            if len(df_old[(df_old["target"] == df_object_new["target"])
                          & (df_old["method_id"] == df_object_new["method_id"])
                          & (df_old["condition"] == df_object_new["condition"])
                          & (df_old["type"] == df_object_new["type"])
                          & (df_old["unit"] == df_object_new["unit"])
                          & (df_old["value"] == df_object_new["value"])]) > 0:
                # print('data exist')
                pass
            elif len(df_old[(df_old["target"] == df_object_new["target"])
                          & (df_old["method_id"] == df_object_new["method_id"])
                          & (df_old["condition"] == df_object_new["condition"])
                          & (df_old["type"] == df_object_new["type"])
                          & (df_old["unit"] == df_object_new["unit"])
                          & (df_old["value"] != df_object_new["value"])]) > 0:
                print(f'{df_object_new["target"]} update data with {df_object_new["type"]}')
            else:
                print(f'{df_object_new["target"]} new data with {df_object_new["type"]}')

        for i in df_new_merge.index:
            # print(df_new_merge.loc[i].to_markdown())
            update_row_data(df_main, df_new_merge.loc[i])
        # df_main_merge = df_main
        # df_main_merge = pd.concat([df_main_merge, df_new_merge], axis=0)
        # print(df_main_merge)
        # df_main_merge.to_excel(path_DB_main, index=None, sheet_name='DB')

    # print(reference_method_table_to_get_method_id("レオメーター"))


def show_main_db_with_target(target: str):
    df_main = pd.read_excel(path_DB_main, sheet_name='DB', index_col=None)
    print(df_main)


if __name__ == "__main__":
    print('save main db system')
    target = input('target: ')
    read_new_df(target)
