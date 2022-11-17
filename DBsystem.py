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
    df_target = pd.read_excel(path_target, sheet_name='target', index_col=None)
    if '-' in target_list[0]:
        target_name = target_list[0].split("-")[0][0:3]
        start_target = target_list[0].split("-")[0][-3:]
        last_target = target_list[0].split("-")[1][-3:]
        # print(target_name, start_target, last_target)
        target_list = [ f'{target_name}' + str('%03d' % (x)) for x in range(int(start_target), int(last_target)+ 1) ]

    print(target_list)
    df_main_temp = df_main
    def get_method_name(x):
        return Service.reference_method_table(x, df_method)

    def get_df_target(df_get_df_target, target:str):
        df_get_df_target = df_get_df_target[df_get_df_target["target"] == target]
        df_get_df_target = df_get_df_target.reset_index(drop=True)
        df_get_df_target["method"] = df_get_df_target["method_id"].apply(get_method_name)
        df_get_df_target.loc[:,target] = df_get_df_target.loc[:,"value"]
        # df_target = df_target.loc[:,['method_id','method','condition','type','unit', target]]
        # print(df_target.to_markdown())
        return df_get_df_target

    def merge_df_col(df_old, df_new):

        # print(df_new)
        # print(df_old)
        for row_index in df_new.index:
            # print(df_new.loc[[row_index],:])
            # print(df_new.at[row_index, 'method_id'])
            if len(df_old[(df_old['method_id'] == df_new.at[row_index, 'method_id']) 
                        & (df_old['condition'] == df_new.at[row_index, 'condition'])
                        & (df_old['type'] == df_new.at[row_index, 'type'])
                        & (df_old['unit'] == df_new.at[row_index, 'unit'])]) > 0:
                # print('add')
                index_of_row_old = df_old[(df_old['method_id'] == df_new.at[row_index, 'method_id']) 
                        & (df_old['condition'] == df_new.at[row_index, 'condition'])
                        & (df_old['type'] == df_new.at[row_index, 'type'])
                        & (df_old['unit'] == df_new.at[row_index, 'unit'])].index.to_list()[0]
                target_temp = str(df_new.at[row_index, "target"])

                df_old.at[index_of_row_old, target_temp] = str(df_new.at[row_index, 'value'])
                
            else:
                df_old = pd.concat([df_old, df_new.loc[[row_index],:]])
                # print('new add')
            
        return df_old
        


    df_show_target = pd.DataFrame({
                            'method_id': pd.Series(dtype='int'),
                           'method': pd.Series(dtype='int'),
                           'condition': pd.Series(dtype='int'),
                           'type': pd.Series(dtype='str'),
                           'unit': pd.Series(dtype='str'),})
    for a_target in target_list:
        df_target = get_df_target(df_main, a_target)
        df_show_target = merge_df_col(df_show_target, df_target)

    def reference_target_list(target_list:list):
        df_target = pd.read_excel(path_target, sheet_name='target', index_col=None)
        df_show_target_list_info = pd.DataFrame()
        for a_target_list in target_list:
            print(a_target_list)
            if len(df_target[df_target["target"] == a_target_list]) > 0:
                target_information = df_target[df_target["target"] == a_target_list]
                df_show_target_list_info = pd.concat([df_show_target_list_info, target_information], axis=0)
            else:
                pass
        return df_show_target_list_info
        

    print(reference_target_list(target_list).to_markdown())
    # print(df_show_target.to_markdown())
    df_show_target = df_show_target.drop(['target','value'], axis=1)
    df_show_target = df_show_target.sort_values(['method_id','condition'])
    print(df_show_target.to_markdown())
        

    # print(df_show_target.to_markdown())
    # print(df_merge_yoko.to_markdown())
    # print(df_target_2)
    # df_target.loc[str(target_list[0])] = df_target.loc[:,["value"]]

if __name__ == "__main__":
    print('DB system')
    # target_list = input('input target: ')
    # show_main_info(target)
    # target_list = ['CBA001-003']
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