import pydicom as pyd
import os
from os.path import join
from os import walk
import glob



def jp2_to_dcm(jp2, dcm):
    # convert from jp2 to dcm file
    # not decompressed
    # libgdcm-tools have to be installed

    cmd_string = 'gdcmimg ' + jp2 + ' ' + dcm  #comand to convert (numpy and pillow needed)
    os.system(cmd_string)


def get_total_files_number(folder):  # helper function

    jp2_list = glob.glob(folder + '/*/*.jp2')
    # add adapt to any folder depth!
    l = len(jp2_list)
    print('{} jp2 files detected'.format(l))
    return l, jp2_list




def convert_dir(convert_dir):
    file_num, file_paths = get_total_files_number(convert_dir)
    # convert and decompress jp2 images in given folder
    # saving in working folder
    n = 1  #
    for path in file_paths:
        img_name = path.split('/')[-1][:-8] #.split('.')[:3]
        #print(img_name, path[:-(len(img_name)+8)])
        source_dcm_path = path[:-(len(img_name)+8)] + 'DICOM/' + img_name + '.dcm'
        ds2 = pyd.dcmread(source_dcm_path, force=True)
        if ds2.ImageType[0] != 'ORIGINAL':
            dcm_path = path[:-8]+'.dcm'
            if not os.path.exists(dcm_path):
                try:
                    jp2_to_dcm(path, dcm_path)
                    ds = pyd.dcmread(dcm_path)
                    ds.decompress()
                    ds.Modality, ds.ImageType = ds2.Modality, ds2.ImageType
                    ds.save_as(dcm_path)
                    n += 1
                    print('converted {}, {} from {}'.format(img_name, n, file_num))
                    try:
                        os.remove(path)
                    except OSError:
                        pass

                except ValueError:
                    print('---' * 20)
                    print('wrong value for {} from {}'.format(img_name, root))
            else:
                print('already exist', img_name)
                n += 1

        else:
            print('ORIGINAL image deleted')
            os.remove(path)
            n += 1



if __name__ == "__main__":
    convert_dir('/media/haimin777/3EFD-EB5D/unpack')
    #get_total_files_number('/media/haimin777/Elements')



