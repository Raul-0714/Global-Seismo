import os
import re

def print_dict(item):
  for key in item:
    if isinstance(item[key], list):
      for element in item[key]:
        print(f'n = {element} ', end='')
      print()
    else:
      print(item[key])


def read_checkmode(i, filename, info_dict):
  
  cwd = os.getcwd() # Get current path
  check_mode_folder = cwd + '/CHECKMODE_OUTPUT_FILES/'
  freq_folder = cwd + '/tmp/'
  input_folder = cwd + '/MINEOS_INPUT_FILES/'

  try:
    with open(check_mode_folder + filename, 'r') as f:
      missing_mode_info = {'filename': filename, 'missing_modes': [], 'missing_modes_num': 0}

      for line in f:
        p1 = re.match(r'^.*Missing.*mode.*$', line)
        p2 = re.match(r'^.*Number.*mode.*$', line)
        if p1:
          missing = re.findall(r'[0-9]+', line)
          missing_mode_info['missing_modes'].append(missing[0])
        if p2:
          num_missing = re.findall(r'[0-9]+', line)
          missing_mode_info['missing_modes_num'] = num_missing[0]
      
      info_dict.append((i, missing_mode_info))

  except IOError:
    print("Can not open the {}".format(filename))     
  except LookupError:
    print("Unknown encoding method")
  except UnicodeDecodeError:
    print("Error occurs when decoding")


def read_freq(missing_modes, info_list):
  cwd = os.getcwd() # Get current path
  check_mode_folder = cwd + '/CHECKMODE_OUTPUT_FILES/'
  freq_folder = cwd + '/tmp/'
  input_folder = cwd + '/MINEOS_INPUT_FILES/'

  print('Reading Frequency')
  for element in missing_modes:
    info_dict = {'l':0, 'num_freq':0, 'freq':[]}
    info_dict['l'] = int(element[0]) 
    info_dict['num_freq'] = int(element[1]['missing_modes_num'])

    freqfile_name = 'premANIC_sph_00000' + str(element[0]) + '.fre'
    try:
      with open(freq_folder + freqfile_name, 'r', encoding='utf-8') as f:
        n = 0
        for line in f:
          line_split = line.split()
          if str(int(line_split[0]) - 1) in element[1]['missing_modes']:
            info_dict['freq'].append(line_split[4])
            n = n + 1
          if n >= int(element[1]['missing_modes_num']):
            break
        info_list.append(info_dict)

    except IOError:
      print("Can not open the {}".format(freqfile_name))
    except LookupError:
      print("Unknown encoding method")
    except UnicodeDecodeError:
      print("Error occurs when decoding")


def main():
  cwd = os.getcwd() # Get current path
  check_mode_folder = cwd + '/CHECKMODE_OUTPUT_FILES/'
  freq_folder = cwd + '/tmp/'
  input_folder = cwd + '/MINEOS_INPUT_FILES/'

# Part I: Read Check_mode files 
  print('Reading Check_mode files')
  missing_modes = [] 
  for i in range(20,60):
    checkmode_name = 'checkmode.sphout_00000' + str(i)    
    read_checkmode(i, checkmode_name, missing_modes) 
  
  
  for element in missing_modes:
    print_dict(element[1])

# Part II: Read Frequency
  freq_dict = [] # The dictionary list to store the frequency information
  read_freq(missing_modes, freq_dict)
  for element in freq_dict:
    print('l = {}'.format(element['l']))
    print(element['freq'])
    print('num = {}'.format(element['num_freq']))

# Part III: Generate New Input Files
  for element in freq_dict:
    inputfile_name = 'mineos.inpsph_00000' + str(element['l'])

    for i in range(0, element['num_freq']):
      new_file_name = inputfile_name + '.' + str(i)

      try:
        with open(input_folder + inputfile_name, 'r', encoding='utf-8') as f: 
          for line in f:
            if re.match(r'^\S+fun$|^\S+fre$', line):
              new_line = re.sub('tmp', 'tmp_m', line)
            elif re.match(r'^\s+\d+\s+\d+\s+.+$', line):
              new_line = re.sub('\s0.\d+',' '+ '3', line)
              new_line = re.sub('\s0\s', ' 5\n', new_line)
            else:
              new_line = line
            
            try:
              with open(input_folder + new_file_name, 'a', encoding='utf-8') as w:
                w.write(new_line)
            except IOError as ex:
              print(ex)
              print('Error ocurred when writing')
            
   
      except IOError:
        print("Can not open the {}".format(inputfile_name))
      except LookupError:
        print("Unknown encoding method")
      except UnicodeDecodeError:
        print("Error occurs when decoding")



if __name__ == '__main__':
  main()
  



  
