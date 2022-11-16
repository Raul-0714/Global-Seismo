import os

S = [(5, 0), (40, 0)]

def ge_num_string(number):
  # This function turns number into a length 7 string
  if number < 10:
    num_str = '000000' + str(number)
  elif number < 100:
    num_str = '00000' + str(number)
  elif number < 1000:
    num_str = '0000' + str(number)
  elif number < 10000:
    num_str = '000' + str(number)
  elif number < 100000:
    num_str = '00' + str(number)
  elif number < 1000000:
    num_str = '0' + str(number)
  else:
    num_str = str(number)

  return num_str 



# Generate input files
def main():
  input_dic = 'tmp/'
  input_file_prefix = 'premANIC_rad_'
  input_file_ext = '.fun'
  tmp_file_name = 'mode_fun.asc'

  for element in S:
    input_file_name = input_dic + input_file_prefix + ge_num_string(element[1]) + input_file_ext
    output_file_name = str(element[0]) + 'S' + str(element[1]) + '.pdf'
    try:
      with open('plot_input.asc', 'a', encoding='utf-8') as w:
        w.write(input_file_name + '\n')
        w.write(tmp_file_name + '\n')
        w.write(str(element[0]) + ' ' + str(element[1]) + '\n')
    except IOError as ex:
      print(ex)
      print('An error occurred when writing')
    
    cmd1 = './read_mineos < plot_input.asc'
    os.system(cmd1)
    cmd2 = './eigT.gmt'
    os.system(cmd2)
    cmd3 = 'mv mode_fun.pdf ' + output_file_name
    os.system(cmd3)
    cmd4 = 'rm plot_input.asc'
    os.system(cmd4)

    




if __name__ == '__main__':
  main()
