import pydicom as pyd
import os
import numpy
from PIL import Image


def jp2_to_dcm(jp2, dcm):
    # convert from jp2 to dcm file
    # not decompressed
    # libgdcm-tools have to be installed

    cmd_string = 'gdcmimg ' + jp2 + ' ' + dcm
    os.system(cmd_string)


def get_total_files_number(folder):  # helper function

    n = 0
    for root, dirs, images in os.walk(folder):

        # print('total files: ', len(images))
        for img in images:
            if img.endswith('.jp2'):
                n += 1
    print('jp2 files number:', n)
    return n


def convert_dir(convert_dir):
    file_num = get_total_files_number(convert_dir)
    # convert and decompress jp2 images in given folder
    # saving in working folder
    n = 1
    for root, dirs, images in os.walk(convert_dir):

        for img in images:
            if img.endswith('.jp2'):
                img_name = img.split('/')[-1][:-8]
                #print(img_name)
                if img_name not in os.listdir(root):
                    ds2 = pyd.dcmread(os.path.join(root, 'DICOM', img_name + '.dcm'), force=True)
                    if ds2.ImageType[0] != 'ORIGINAL':
                        try:
                            jp2_to_dcm(os.path.join(root, img), os.path.join(root, img_name))
                            ds = pyd.dcmread(os.path.join(root, img_name))
                            ds.decompress()
                            ds.Modality, ds.ImageType = ds2.Modality, ds2.ImageType
                            ds.save_as(os.path.join(root, img_name))
                            n += 1
                            print('converted {}, {} from {}'.format(img, n, file_num))
                        except ValueError:
                            print('---' * 20)
                            print('wrong value for {} from {}'.format(img, root))


                    else:
                        print('ORIGINAL image skipped')
                        n += 1
                else:
                    print('already exist', img_name)
                    n += 1
                    # dir_list.append(root.split('/')[-1])


if __name__ == "__main__":
    convert_dir('/home/haimin/Dicom/pacs/59586')

