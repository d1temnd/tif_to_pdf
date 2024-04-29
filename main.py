import shutil
from PIL import Image, ImageSequence, ImageFile
import easygui
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


def tiff_to_pdf(tiff_path: str, pdf_folder: str) -> str:
    pdf_path = os.path.join(pdf_folder, os.path.basename(tiff_path).replace('.tiff', '.pdf'))
    if not os.path.exists(tiff_path):
        raise Exception(f'{tiff_path} does not exist.')
    image = Image.open(tiff_path)

    images = []
    for i, page in enumerate(ImageSequence.Iterator(image)):
        page = page.convert("RGB")
        images.append(page)

    if len(images) == 1:
        images[0].save(pdf_path)
    else:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])

    return pdf_path


# print(tiff_to_pdf("3.tiff"))


def remuvTMP(file_list: list, source_folder: str, save_file_dir: str):
    # Создаем папку "tmp" в абсолютном пути
    tmp_folder = os.path.join(source_folder, "tmp")
    os.makedirs(tmp_folder, exist_ok=True)

    # Копирование файлов и смена расширения
    for file in file_list:
        file_name, file_ext = os.path.splitext(os.path.basename(os.path.join(source_folder, file)))
        new_file_name = os.path.join(tmp_folder, file_name + ".tiff")
        shutil.copyfile(os.path.join(source_folder, file), new_file_name)

    # Получаем список файлов в папке "tmp"
    katalog_file = os.listdir(tmp_folder)

    return katalog_file, [tmp_folder, save_file_dir]


def interfase():
    first_window = easygui.indexbox(msg='Выберете как открыть папку', title='ttp - tiff to pdf',
                                    choices=('Путь', 'Проводник', 'Текущая'))

    if first_window == 0:
        past = easygui.multenterbox(msg='Введите путь до папки', title='ttp - tiff to pdf',
                                    fields=["Папка с tiff: ",
                                            "Папка для сохранения pdf: "])

        files_all = os.listdir(past[0])
        filtered_files = list(filter(lambda x: x.lower().endswith(".tif") or x.lower().endswith(".tiff"), files_all))

        return filtered_files, past  # [path input, path_output]


    elif first_window == 1:
        past = easygui.diropenbox(title="ttp - tiff to pdf", msg="Выберите папку")
        files_all = os.listdir(past)

        filtered_files = list(filter(lambda x: x.lower().endswith(".tif") or x.lower().endswith(".tiff"), files_all))

        return filtered_files, [past, rf'{past}']

    elif first_window == 2:
        files_all = os.listdir()
        file_pash = os.path.abspath(files_all[0])
        # index = os.path.abspath(files_all[1]).rsplit('/', 1)[0]
        # print(index)
        past = os.path.dirname(file_pash)
        # print(past)
        filtered_files = list(filter(lambda x: x.lower().endswith(".tif") or x.lower().endswith(".tiff"), files_all))

        return filtered_files, [past, rf'{past}']


def main():
    try:
        file_list = interfase()
        exm = remuvTMP(file_list[0], file_list[1][0], file_list[1][1])

        os.makedirs(rf'{exm[1][1]}\pdf', exist_ok=True)
        print(file_list)
        print(exm)
        for file in exm[0]:
            tiff_to_pdf(rf'{exm[1][0]}\{file}', rf"{exm[1][1]}\pdf")
            print(file, ": file okk")

        for delete_file in exm[0]:
            os.remove(rf"{exm[1][0]}\{delete_file}")
        os.rmdir(rf'{exm[1][0]}')

        easygui.msgbox(title="ttp - tiff to pdf", msg=rf"Конвертировано успешно. {exm[1][1]}\pdf")


    except TypeError:
        print("не передан путь(закрытв программа)")


# ([файлы_tif], ["путь откуда", "путь куда"])

if __name__ == '__main__':
    main()
