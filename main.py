def fit_linear(filename):
    str = open_read_file(filename)
    str_lists = organize_str(str)
    y_axis_titles = str_lists.pop() # save for the plot
    x_axis_titles = str_lists.pop() # save for the plot
    str_dict = check_version_transpose_to_dict(str_lists)
    if test_dict(str_dict) == 1:  # if there is an error, now its soppused to print the kind of it
        return
    avg_dict = calculation_avg(str_dict)
    dict_of_outputs = calculation_a_da_b_db(avg_dict)
    dict_of_outputs.update(calculation_chi_square_snd_red(dict_of_outputs,str_dict))
    y_dots_to_plot = calculation_of_the_straight_formula(str_dict, dict_of_outputs)

    from matplotlib import pyplot # create the graph from the data:
    pyplot.plot(str_dict['x'],y_dots_to_plot,color='red')
    pyplot.errorbar(str_dict['x'],str_dict['y'],xerr=str_dict['dx'],yerr=str_dict['dy'],ecolor='blue',fmt='None')
    pyplot.xlabel(''.join(x_axis_titles[2:]))
    pyplot.ylabel(''.join(y_axis_titles[2:]))
    pyplot.savefig("linear_fit.svg")
    pyplot.show()

    #print (str)
    #print (str_lists)
    #print (str_dict)
    #print (x_axis_titles)
    #print (y_axis_titles)
    #print (avg_dict)
    #print (dict_of_outputs)
    print ('Evaluated fitting parameters:''\n''a=',dict_of_outputs['a'],'+-',dict_of_outputs['da'],'\n''b=',dict_of_outputs['b'],'+-',dict_of_outputs['db'],'\n''chi2=',dict_of_outputs['chi_square'],'\n''chi2_reduced=',dict_of_outputs['chi_square_red'])

    return

def open_read_file (filename): # input: file
    my_file = open(filename, 'r')
    str = my_file.readlines()
    my_file.close()
    return str  # output: list of strings, each index contain one line

def organize_str (str): # input: list of strings
    str_lists=[]
    for line in str:
        newline =line.replace('\n',"") # remove \n
        newlinelow=newline.lower()     # switch to lower cases
        newlinelow = list(newlinelow.split(" "))  # split into lists
        if newlinelow!=['']:  # if the list isn't empty, append into the list of lists
            str_lists.append(newlinelow)
    return str_lists  # output: organized list of string lists

def check_version_transpose_to_dict(str_lists): # input: list of string lists
    if len(str_lists[0])==4 and 'x' in str_lists[0] and 'dx' in str_lists[0] and 'y' in str_lists[0] and 'dy' in str_lists[0]: # chack if matrix arranged by columns
        fixed_str = [[str_lists[j][i] for j in range(len(str_lists))] for i in range(len(str_lists[0]))]  # matrix transpose
        str_dic = {dot[0]: dot[1:] for dot in fixed_str} # convert to dict
    else: #If the matrix is already arranged in rows
        str_dic = {dot[0]: dot[1:] for dot in str_lists}  # convert to dict
    for key in str_dic: # remove all the empty dots from each key
        for dot in str_dic[key]:
            if dot=='':
                str_dic[key].remove(dot)
    for each_key in str_dic:    # convert values to float
        str_dic[each_key] = [float(i) for i in str_dic[each_key]]
    str_dic['N']=len(str_dic['x'])  # for the lest calculation the num of dots will needed in this dict too
    return str_dic # output: dict with keys 'x','y','dy','dx' and the values in each key are floats + key 'N' with value num of dots

def test_dict (str_dic): # input: dict with x,y,dx,dy keys
    if not len(str_dic['x'])== len(str_dic['y']) == len(str_dic['dx']) == len(str_dic['dy']): # check if all the keys have the same amount of values
        print('Input file error: Data lists are not the same length.')
        return 1
    for dot in str_dic['dx']: # check if values in key 'dx' are positive
        if dot<0:
            print('Input file error: Not all uncertainties are positive.')
            return 1
    for dot in str_dic['dy']: # check if values in key 'dy' are positive
        if dot<0:
            print('Input file error: Not all uncertainties are positive.')
            return 1
    return 0 # output: 0 or 1

def calculation_avg (str_dict):  # input: the dict with keys x,y,dx,dy that pass the test
    dict_of_avg={}  # a dict that will contain eventually the weighted average of x y x_square dy_square xy_product
    dy_square_list=[] # arrange dy_square for dict
    for dot in str_dict['dy'] :
        dy_square_list.append(dot**2)
    dict_of_avg['dy_square']=dy_square_list
    x_square_list=[] # arrange x_square for dict
    for dot in str_dict['x']:
        x_square_list.append(dot ** 2)
    dict_of_avg['x_square']=x_square_list
    dict_of_avg['x']=str_dict['x'] # arrange x for dict
    dict_of_avg['y']=str_dict['y'] # arrange y for dict
    N=len(dict_of_avg['x'])   # num of dots
    dict_of_avg['xy_product']=[x*y for x,y in zip (str_dict['x'],str_dict['y'])] # arrange xy_product for dict
    sum_of_one_divide_by_dy_square=0 # the lower organ in the the division operation to get the weighted average
    for dot in dict_of_avg['dy_square']:
       sum_of_one_divide_by_dy_square=sum_of_one_divide_by_dy_square+(1/dot)
    for every_key in dict_of_avg: # update the values in the keys from list to float of the weighted average
        every_key_divde_by_dy_square =[x/y for x,y in zip (dict_of_avg[every_key], dy_square_list)]
        sum_of_every_key_divde_by_dy_square=sum(every_key_divde_by_dy_square) # the upper organ in the the division operation to get the weighted average
        dict_of_avg[every_key]= sum_of_every_key_divde_by_dy_square/sum_of_one_divide_by_dy_square # the upper sum diveded by the lower sum
    dict_of_avg['N']=N # after all the values update, append key N to the dict with his value (num of dots)
    return dict_of_avg # output: new dict with the keys x,y,dy_square,xy_product and their values are their wighted avg + key 'N' with value num of dots

def calculation_a_da_b_db(dict_of_avg): # input: dict with the wighted avg
    import math
    dict_of_outputs={}
    a=(((dict_of_avg['xy_product']-((dict_of_avg['x'])*(dict_of_avg['y'])))/((dict_of_avg['x_square'])-((dict_of_avg['x'])**2))))
    dict_of_outputs['a']=a
    da= math.sqrt((dict_of_avg['dy_square'])/((dict_of_avg['N'])*((dict_of_avg['x_square'])-((dict_of_avg['x'])**2))))
    dict_of_outputs['da'] = da
    b=((dict_of_avg['y'])-(a*(dict_of_avg['x'])))
    dict_of_outputs['b'] = b
    db=math.sqrt(((dict_of_avg['dy_square'])*(dict_of_avg['x_square']))/((dict_of_avg['N'])*((dict_of_avg['x_square'])-((dict_of_avg['x'])**2))))
    dict_of_outputs['db'] = db
    return dict_of_outputs # output: new dic with the keys 'a','b','da','db', their values are the result of the calculation

def calculation_chi_square_snd_red(dict_of_outputs,str_dict): # dict of outputs
    dict_of_chi_square ={}
    list_new_x=[]
    for every_dot in str_dict['x']: # for every dot_x multiply by a and add b. append to new list
        every_dot=((every_dot*dict_of_outputs['a'])+(dict_of_outputs['b']))
        list_new_x.append(every_dot)
    list_y_less_x=[y-x for y,x in zip (str_dict['y'],list_new_x)] # every dot_y reduse dot_x and appenend the result to new list
    list_of_result_of_division=[(dot/dy)**2 for dot,dy in zip (list_y_less_x,str_dict['dy'])] # every dot in the new list divide by dot dy
    chi_square=sum(list_of_result_of_division)
    dict_of_chi_square['chi_square'] = chi_square
    chi_square_red=((chi_square)/((str_dict['N'])-2))
    dict_of_chi_square['chi_square_red']=chi_square_red
    return dict_of_chi_square # output: dict of outputs updated with new keys

def calculation_of_the_straight_formula(str_dict,dict_of_outputs): # input: dict of outputs and list of lists (dots)
    y_dots_to_plot=[]
    for every_dot in str_dict['x']:
        newdot = (every_dot *dict_of_outputs['a']) + dict_of_outputs['b']
        y_dots_to_plot.append(newdot)
    return (y_dots_to_plot)  # output: lists of dots will be the y dots (for the line) that will enter to the graph

#if __name__== '__main__':    # way to check the main function with a selected text file
#      fit_linear('input.txt')