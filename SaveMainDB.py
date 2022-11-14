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
    path_new = os.path.expanduser('~/Desktop') + f'/{target} Data/{target} Data.xlsx'
    df_new = pd.read_excel(path_new, sheet_name='Sheet1', index_col=0)
    # print(df_new.columns.to_list()[4:])
    target_list: list[str] = df_new.columns.to_list()[4:]

    def reference_method_table_to_get_method_id(a):
        if a == "" or a == None:
            return 89

        a_first_name = re.split('[_ ]', a)[0]
        # print(len(df_method[df_method["method_name"].str.contains(a_first_name)]["id"]))
        if len(df_method[df_method["method_name"].str.contains(a_first_name)]["id"]) > 0:
            id_method = df_method[df_method["method_name"].str.contains(a_first_name)]["id"].to_list()[0]
            return id_method
        else:
            return 99
    

    for a_target in target_list:

        df_main = pd.read_excel(path_DB_main, sheet_name='DB', index_col=None)
        # print(a_target)
        df_new_temp = df_new
        df_new_temp["value"] = df_new_temp[a_target]
        df_new_temp["target"] = a_target
        df_new_temp["method_id"] = df_new_temp["method"].apply(reference_method_table_to_get_method_id)
        # print(df_new_temp.loc[:, ["target" ,'method', 'condition', 'type', 'unit', "value"]])
        # print(df_new_temp)
        df_new_merge = df_new_temp.loc[:, ["target" ,'method_id', 'condition', 'type', 'unit', "value"]]
        df_main_merge = df_main
        df_main_merge = pd.concat([df_main_merge, df_new_merge], axis=0)
        # print(df_main_merge)
        df_main_merge.to_excel(path_DB_main, index=None, sheet_name='DB')
        

    # print(reference_method_table_to_get_method_id("レオメーター"))

def show_main_db_with_target(target:str):
    df_main = pd.read_excel(path_DB_main, sheet_name='DB', index_col=None)
    print(df_main)





if __name__ == "__main__":
    print('save main db system')
    target  = input('target: ')
    read_new_df(target)