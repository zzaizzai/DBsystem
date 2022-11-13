import pandas as pd
import os


path_DB_main = os.path.expanduser('~/Desktop') + '/DBsystem/DB_main.xlsx'
path_method = os.path.expanduser('~/Desktop') + '/DBsystem/DB_method.xlsx'
path_target = os.path.expanduser('~/Desktop') + '/DBsystem/DB_target.xlsx'

if not os.path.isfile(path_DB_main) or not os.path.isfile(path_method) or not os.path.isfile(path_target):
    print('no data file')
    print('create new file')
    df_new = pd.DataFrame({'target': pd.Series(dtype='str'),
                           'method_id': pd.Series(dtype='int'),
                           'condition': pd.Series(dtype='int'),
                           'type': pd.Series(dtype='str'),
                           'unit': pd.Series(dtype='str'),
                            'value': pd.Series(dtype='float')})

    df_new_2 = pd.DataFrame({
                           'id': pd.Series(dtype='int'),
                           'method_name': pd.Series(dtype='str')})

    df_new_3 = pd.DataFrame({'target': pd.Series(dtype='str'),
                           'kind': pd.Series(dtype='str'),
                           'recipe': pd.Series(dtype='str'),})

    df_new.to_excel(path_DB_main,sheet_name='DB', index=False)
    df_new_2.to_excel(path_method,sheet_name='method', index=False)
    df_new_3.to_excel(path_target,sheet_name='target', index=False)


df_main = pd.read_excel(path_DB_main, sheet_name='DB', index_col=None)
df_method = pd.read_excel(path_method, sheet_name='method', index_col=None)
df_target = pd.read_excel(path_target, sheet_name='target', index_col=None)

print(df_main)
print(df_method)
print(df_target)


def reference_method_table(a):
    return df_method[df_method["id"] == a]["method_name"].to_list()[0]

def reference_target_kind_table(a):
    return df_target[df_target["target"] == a]["kind"].to_list()[0]

df_main["method"] = df_main["method_id"].apply(reference_method_table)
df_main["rubber"] = df_main["target"].apply(reference_target_kind_table)


# print(df_main.loc[:,['target' ,'method']])
print(df_main)
