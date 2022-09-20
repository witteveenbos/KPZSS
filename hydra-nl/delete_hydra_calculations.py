import os, shutil


hydra_werkmap = r'C:\MyPrograms\Hydra-NL_KP_ZSS\werkmap'

for folder in os.listdir(hydra_werkmap):

    # geïnteresseerd in de data van generieke database-namen
    string_to_match = ["Westerschelde", "Waddenzee", "Hollandse_Kust"]

    for substring in string_to_match:
        if substring in folder:
            folder_path = os.path.join(hydra_werkmap, folder)
            for map in os.listdir(folder_path):
                if 'Shapes' in map:
                    print('shapes doen we niet')
                elif os.path.isdir(os.path.join(hydra_werkmap, folder, map)):
                    shutil.rmtree(os.path.join(hydra_werkmap, folder, map))
                # print(map)
                # if 'Shapes' in os.path.join(hydra_werkmap, folder, map):
                #     print('Shape file doen we niet')
                # elif os.path.isdir(os.path.join(hydra_werkmap, folder, map)):
                #     print(map)



# for filename in os.listdir(folder):
#     file_path = os.path.join(folder, filename)
#     try:
#         if os.path.isfile(file_path) or os.path.islink(file_path):
#             os.unlink(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     except Exception as e: