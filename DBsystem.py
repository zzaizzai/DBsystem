import pandas as pd
import os
import Service


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


# df_main = pd.read_excel(path_DB_main, sheet_name='DB', index_col=None)
# df_method = pd.read_excel(path_method, sheet_name='method', index_col=None)
# df_target = pd.read_excel(path_target, sheet_name='target', index_col=None)


def show_main_info(target: str):
    df_main = pd.read_excel(path_DB_main, sheet_name='DB', index_col=None)
    df_method = pd.read_excel(path_method, sheet_name='method', index_col=None)
    df_target = pd.read_excel(path_target, sheet_name='target', index_col=None)

    def reference_method_table(a):
        if len(df_method[df_method["id"] == a]["method_name"]) > 0:
            return df_method[df_method["id"] == a]["method_name"].to_list()[0]
        else:
            return None

    def reference_target_kind_table(a):
        if len(df_target[df_target["target"] == a]["kind"]) > 0:
            rubber = df_target[df_target["target"] == a]["kind"].to_list()[0]
            return rubber
        else:
            return None
    def refernce_target_information(a):
        if len(df_target[df_target["target"] == a]) > 0:
            target_information = df_target[df_target["target"] == a]
            return target_information
        else:
            return


    df_main["method"] = df_main["method_id"].apply(reference_method_table)
    # df_main["rubber"] = df_main["target"].apply(reference_target_kind_table)

    

    # print(df_main.loc[:,['target' ,'method']])
    print(refernce_target_information(target).to_markdown())
    print(df_main[df_main["target"] == str(target) ].loc[:,["target","method","condition", "type", "unit","value"]].to_markdown())

def show_main_info_compare(target_list:list):
    df_main = pd.read_excel(path_DB_main, sheet_name='DB', index_col=None)
    df_method = pd.read_excel(path_method, sheet_name='method', index_col=None)
    df_target_1 = pd.read_excel(path_target, sheet_name='target', index_col=None)
    if '-' in target_list[0]:
        target_name = target_list[0].split("-")[0][0:3]
        start_target = target_list[0].split("-")[0][-3:]
        last_target = target_list[0].split("-")[1][-3:]
        # print(target_name, start_target, last_target)
        target_list = [ f'{target_name}' + str('%03d' % (x)) for x in range(int(start_target), int(last_target)+ 1) ]

    print(target_list)
    df_main_temp = df_main
    def get_method_name(x):
        Service.reference_method_table(x, df_method)
        return
    df_target_1 = df_main_temp[df_main_temp["target"] == target_list[0]]
    df_target_1 = df_target_1.reset_index(drop=True)
    # df_target_1["method"] = df_target_1["method_id"].apply(get_method_name)
    df_target_1.loc[:,target_list[0]] = df_target_1.loc[:,"value"]
    df_target_1 = df_target_1.loc[:,['condition','type','unit',target_list[0]]]
    print(df_target_1)

    df_target_2 = df_main_temp.loc[df_main_temp["target"] == target_list[1],:]
    df_target_1 = df_target_1.reset_index(drop=True)
    # df_target_2["method_name"] = df_target_2["method_id"]
    # df_target_2["method"] = df_target_2["method_id"].apply(get_method_name)
    df_target_2[target_list[1]] = df_target_2["value"]
    df_target_2 = df_target_2.loc[:,['condition','type','unit', target_list[1]]]
    print(df_target_2)

    df_merge_yoko = pd.merge(df_target_1,df_target_2, on=['method','condition','type','unit'], how='outer')
    print(df_merge_yoko.to_markdown())
    # print(df_target_2)
    # df_target.loc[str(target_list[0])] = df_target.loc[:,["value"]]

if __name__ == "__main__":
    print('DB system')
    # target = input('input target: ')
    # show_main_info(target)
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

    show_main_info_compare(target_list)