import pydicom as pyd

def jp2_to_dcm(jp2, dcm):
        # convert from jp2 to dcm file
        # not decompressed

      cmd_string = 'gdcmimg ' + jp2 + ' ' + dcm
      files.os.system(cmd_string)
      
def get_total_files_number(folder):
        
        n=0
        for root, dirs, images in files.os.walk(folder):
          
          #print('total files: ', len(images))
          for img in images:
            if img.endswith('.jp2'):
                      n += 1
        print('jp2 files number:', n)
        return n

      
def convert_dir(convert_dir):
        file_num = get_total_files_number(convert_dir)
        # convert and decompress jp2 images in given folder
        n = 1
        for root, dirs, images in files.os.walk(convert_dir):

            for img in images:
                if img.endswith('.jp2'):
                    img_name = img.split('/')[-1][:-8]
                    #print(img_name)
                    if img_name not in files.os.listdir(root):
                      ds2 = pyd.dcmread(files.os.path.join(root, 'DICOM', img_name + '.dcm'), force=True)
                      if ds2.ImageType[0] != 'ORIGINAL':
                        try:
                          jp2_to_dcm(files.os.path.join(root, img), files.os.path.join(root, img_name))
                          ds = pyd.dcmread(files.os.path.join(root, img_name))
                          ds.decompress()
                          ds.Modality, ds.ImageType = ds2.Modality, ds2.ImageType
                          ds.save_as(files.os.path.join(root, img_name))
                          n +=1
                          print('converted {}, {} from {}'.format(img, n, file_num))
                        except ValueError:
                          print('---'*20)
                          print('wrong value for {} from {}'.format(img, root))


                      else:
                        #print('ORIGINAL image skipped')
                        n+=1
                    else:
                      #print('already exist')
                      n+=1 
                      #dir_list.append(root.split('/')[-1])
      

