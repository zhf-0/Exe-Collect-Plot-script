#!/usr/bin/env python3
import re
import os 
import subprocess
import time
import argparse
import numpy as np
import itertools
import random
import operator

def IsNumerical(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class Running:
    def __init__(self,e_path,size,TemplateInput,keys,vals):
        log_name = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        log_path = os.path.join(os.getcwd(),'log',log_name)
        count = 1
        while os.path.exists(log_path):
            log_path = log_path+'_'+str(count) 
            count = count + 1
        os.makedirs(log_path)
        
        self.log_path = log_path
        self.batch_size = size 
        self.exec_path = e_path 

        self.config = {}
        self.input = TemplateInput
        self.keys = keys
        self.vals = vals
        self.output_config = os.path.join(self.log_path,'config.dat')

        self.max_it = 1000
        self.max_time = 10000.0
        self.iterations = []
        self.elapse_times = []
        self.residuals = []
        self.grid_complexity = []
        self.operator_complexity = []

        self.average_time = 0
        self.average_iter = 0
        self.average_resi = 0
        self.average_grid_com = 0
        self.average_oper_com = 0

    def ParseInputConfig(self):
        with open(self.input,'r') as f:
            contents = f.readlines()

        for line in contents:
            if re.search('%',line):
                line = line.split('%')[0].strip()

            if re.search('=',line):
                items = line.split('=')
                key = items[0].strip()
                val = items[1].strip()
                self.config[key] = val

    def OutputConfig(self):
        for i in range(len(self.keys)):
            self.config[self.keys[i]] = self.vals[i]

        contents = []
        for k,v in self.config.items():
            line = '{:<25} = {:<25} \n'.format(k,v)
            contents.append(line)

        with open(self.output_config,'w') as f:
            f.writelines(contents)

    def BatchExec(self):
        self.ParseInputConfig()
        self.OutputConfig()
        cmd = self.exec_path +' -ini '+self.output_config

        for i in range(self.batch_size):
            try:
                run_output = subprocess.check_output(cmd,shell=True)
            except subprocess.CalledProcessError as error:
                print('\033[31m running fail! :','check the log dir {} \033[0m'.format(self.log_path))
                print(error.output.decode('utf-8'))
                # contents = error.output.decode('utf-8')
                contents = ['Number of iterations = {} with relative residual 0.\n'.format(self.max_it),'AMG_Krylov method totally costs {} seconds\n'.format(self.max_time)]
            else:
                contents = run_output.decode('utf-8')
            finally:
                local_log_path = os.path.join(self.log_path,str(i)+'.log')
                with open(local_log_path,'w') as f:
                    f.write(contents)
                    change_list = ['\n','='*75,'\n']
                    for k in range(len(self.keys)):
                        tmp_line = '{:<25} = {:<25} \n'.format(self.keys[k],self.vals[k])
                        change_list.append(tmp_line)

                    f.writelines(change_list)

                lines = contents.split('\n')
                for line in lines:
                    if re.search('iterations',line):
                        self.iterations.append(eval(line.split()[4]))
                        self.residuals.append(eval(line.split()[-1].strip('.')))
                    if re.search('MaxIt',line):
                        self.iterations.append(eval(line.split()[4]))
                        self.residuals.append(eval(line.split()[-1].strip('.')))
                    if re.search('totally',line):
                        self.elapse_times.append(eval(line.split()[4]))
                    if re.search('complexity',line):
                        self.grid_complexity.append(eval(line.split()[3]) )
                        self.operator_complexity.append(eval(line.split()[-1]) )

    def CollectInfo(self):
        # the target is iteration, if the target is elapsed time, change the if-else condition as follow
        result_len = len(self.iterations)
        if result_len == 0:
            print('\033[31m can not collect the info : the len of result is 0, check the log dir {} \033[0m'.format(self.log_path))
            self.average_iter = self.max_it
            self.average_time = self.max_time
            self.average_resi = 0.0
            self.average_grid_com = 0.0
            self.average_oper_com = 0.0
        else:
            for i in range(result_len):
                if not IsNumerical(self.iterations[i]):
                    print('\033[31m the value is not a number, check the log dir {} \033[0m'.format(self.log_path))
                    self.iterations[i] = self.max_it
                elif self.iterations[i] == 0: 
                    print('\033[31m the value is 0, check the log dir {} \033[0m'.format(self.log_path))
                elif abs( self.iterations[i] - self.iterations[0] ) > 5:
                    print("be careful! the iterations[{}] changes rapidly".format(i))

            self.average_time = sum(self.elapse_times) / result_len
            self.average_iter = sum(self.iterations) / result_len
            self.average_resi = sum(self.residuals) / result_len
            self.average_grid_com = sum(self.grid_complexity) / result_len 
            self.average_oper_com = sum(self.operator_complexity) / result_len 


def FinalProcess(keys,vals,grid_path):
    batch_size = 1
    exec_path = './test'
    input_path = './input.dat'

    grid_contents = []
    total_par  = []
    total_time = []
    total_iter = []
    total_resi = []
    for item in itertools.product(*vals):
        a = Running(exec_path,batch_size,input_path,keys,item)
        a.BatchExec()
        a.CollectInfo()
        out = "when parameter = {}; num of iter = {}; the elapsed time = {}; the residual = {}; grid complexity = {}; operator complexity = {}; the log path is : {}".format(item,a.average_iter,a.average_time,a.average_resi,a.average_grid_com,a.average_oper_com,a.log_path)
        print(out,flush=True)

        grid_contents.append(out+'\n')
        total_par.append(item)
        total_time.append(a.average_time)
        total_iter.append(a.average_iter)
        total_resi.append(a.average_resi)


    min_index, min_number = min(enumerate(total_iter), key=operator.itemgetter(1))

    out1 = "\n===================================================="
    opt_out = "when parameter = {}; num of iter = {}; the elapsed time = {}; the residual = {}".format(total_par[min_index],total_iter[min_index],total_time[min_index],total_resi[min_index])
    out2 = "====================================================\n"

    grid_contents.append(out1+'\n')
    grid_contents.append(opt_out+'\n')
    grid_contents.append(out2+'\n')

    if grid_path != 0:
        with open(grid_path,'w') as f:
            f.writelines(grid_contents)
    

    print(out1)
    print(opt_out)
    print(out2)

def GenList(begin,step,end):
    a = [begin]
    while begin + step < end:
        begin = begin + step
        a.append(begin)

    a.append(end)
    return a

if __name__ == "__main__":

    # this is for threshold
    #=============================================================
    keys = ['workdir','AMG_strong_threshold']
    
    list1 = ['./5/'] 
    
    # list2 = list(np.linspace(0.01,0.99,99,endpoint=True))
    list2 = GenList(0.001,0.001,0.1)

    vals = [list1,list2]

    FinalProcess(keys,vals,list1[0]+'refined_threshold_grid.txt')
    #=============================================================

    # this is for jacobi weight
    #=============================================================
    # keys = ['workdir','AMG_smoother','AMG_relaxation']

    # list1 = ['./5/'] 
    # # list1 = [0]

    # list2 = ['JACOBI']

    # list3 = list(np.linspace(0.01,0.99,99,endpoint=True))
    # # list3 = list(np.linspace(0.5,0.98,49,endpoint=True))

    # vals = [list1,list2,list3]

    # FinalProcess(keys,vals,'./5/test_relax_grid.txt')
    # for i in range(5,17):
    #     list1[0] = './{}/'.format(i)
    #     vals = [list1,list2,list3]
    #     f_name = list1[0]+'relax_grid.txt'
    #     FinalProcess(keys,vals,f_name)
    #=============================================================

    # thsi is for thershold + jacobi weight
    # keys = ['workdir','AMG_smoother','AMG_relaxation','AMG_strong_threshold']

    # list1 = ['./16/'] 

    # list2 = ['JACOBI']

    # list3 = list(np.linspace(0.5,0.98,49,endpoint=True))

    # list4 = list(np.linspace(0.1,0.9,81,endpoint=True))

    # vals = [list1,list2,list3,list4]

    # FinalProcess(keys,vals,list1[0]+'relax_threshold_grid.txt')
