#!/usr/bin/python3
import os
import csv
import random
import argparse
from subprocess import call
from datetime import datetime
from os.path import exists

def run_call(cmd,execute_call=True):
    cmd_f=open(regression_cmds,'a')
    if (execute_call):
        print(" ".join(map(str,cmd)),file=cmd_f)
    else:
        print(cmd,file=cmd_f)
    cmd_f.close()
    if (execute_call):
        call(cmd)
    else:
        os.system(cmd)
def get_list(string):
    return list(string.split(" "))
def report_regression_results(update):
    if (update):
        yet_to_run_count = 0
        completed_count = 0
        pass_logs = []
        fail_logs = []
        timeout_logs = []
        for log in logs:
            if(exists(log)):
                completed_count += 1
            else:
                yet_to_run_count += 1
                continue
            file = open(log, "r")
            readfile = file.read()
            if PASS_STR in readfile: 
                pass_logs.append(log)
                pass_ucdb_l = '/'.join((log.split("/"))[:-1])+'/'+(log.split("/"))[-2]+'.ucdb'
                pass_ucdbs.append(pass_ucdb_l)
            elif FAIL_STR in readfile:
                fail_logs.append(log)
            elif TIMEOUT_STR in readfile:
                timeout_logs.append(log)
            elif FAIL_STR2 not in readfile:
                fail_logs.append(log)
            else :
                unknown_logs.append(log)
            file.close()
        f=open(regression_report_file,'w')
        if (len(pass_logs)):
            print("\n********    PASSED LOGS    ********",file=f)
            i = 0
            for log in pass_logs:
                i += 1
                print(str(i),"\t:",log,file=f)
        if (len(fail_logs)):
            print("\n********    FAILED LOGS    ********",file=f)
            i = 0
            for log in fail_logs:
                i += 1
                print(str(i),"\t:",log,file=f)
        if (len(timeout_logs)):
            print("\n********   TIMEOUT LOGS    ********",file=f)
            i = 0
            for log in timeout_logs:
                i += 1
                print(str(i),"\t:",log,file=f)
        if (len(unknown_logs)):
            print("\n********   UNKNOWN LOGS    ********",file=f)
            i = 0
            for log in unknown_logs:
                i += 1
                print(str(i),"\t:",log,file=f)
        print("\n******** Regression Report ********",file=f)
        print("Passed :",str(len(pass_logs)   ),file=f)
        print("Failed :",str(len(fail_logs)   ),file=f)
        print("Timeout:",str(len(timeout_logs)),file=f)
        print("Unknown:",str(len(unknown_logs)),file=f)
        print("To Run :",str(yet_to_run_count ),file=f)
        print("Total  :",str(len(logs)        ),file=f)
        print("Pass % :",str(round(len(pass_logs)/len(logs)*100,1)),file=f)
        print("***********************************\n",file=f)
        print("Note : To run the same regression \nmake regress TESTLIST="+regression_test_list+"\n",file=f)
        f.close()
    f = open(regression_report_file,"r")
    file_contents = f.read()
    print(file_contents)
    f.close()
def apply_exclution():
    global pass_ucdb
    global cov_path
    global exclude_csv
    pass_combined_exclusion_do_file = regression_path+"/cov/pass_exclusion.do"
    all_combined_exclusion_do_file = regression_path+"/cov/all_exclusion.do"
    pass_cov_merge_file = cov_path + "/pass_cov_merge.txt "
    all_cov_merge_file = cov_path + "/all_cov_merge.txt "
    pass_report_do_switches_html = "\ncoverage report -html -output " + cov_path + \
    "/pass_covhtmlreport_with_waivers -annotate -details -assert -directive -cvg -code bcefst -threshL 50 -threshH 90\nexit\n"
    all_report_do_switches_html = "\ncoverage report -html -output " + cov_path + \
    "/all_covhtmlreport_with_waivers -annotate -details -assert -directive -cvg -code bcefst -threshL 50 -threshH 90\nexit\n"
    pass_report_do_switches_txt = "\ncoverage report -assert -directive -cvg -code bcefst -output " + pass_cov_merge_file 
    all_report_do_switches_txt  = "\ncoverage report -assert -directive -cvg -code bcefst -output " + all_cov_merge_file 
    pass_cexc_f=open(pass_combined_exclusion_do_file,'a')
    all_cexc_f =open(all_combined_exclusion_do_file,'a')
    exc_f = open(exclude_file, "r")
    mexc_f = open(manual_exclude_file, "r")
    for line in exc_f:
        pass_cexc_f.write(line)
        all_cexc_f.write(line)
    pass_cexc_f.write("\n")
    all_cexc_f.write("\n")
    rtl_path = os.getcwd()+"/../../"
    rtl_abs_path = os.path.abspath(rtl_path)
    pass_cexc_f.write("set DESIGN_PATH " + rtl_abs_path + " \n")
    all_cexc_f.write ("set DESIGN_PATH " + rtl_abs_path + " \n")
    exc_f=open(exclude_csv,'r')
    exc_dict = csv.DictReader(exc_f)
    for exc in exc_dict:
        if("#" in exc['FILE']):
            continue
        file_abs =  "$DESIGN_PATH/" + exc['FILE']
        print("coverage exclude -src " + file_abs + " -line " + exc['LINE']+ " -code " + exc['EXCLUSION_TYPES'],file=pass_cexc_f)
        print("coverage exclude -src " + file_abs + " -line " + exc['LINE']+ " -code " + exc['EXCLUSION_TYPES'],file=all_cexc_f)
    for line in mexc_f:
        pass_cexc_f.write(line)
        all_cexc_f.write(line)
    pass_cexc_f.write(pass_report_do_switches_txt)
    all_cexc_f.write(all_report_do_switches_txt)
    pass_cexc_f.write(pass_report_do_switches_html)
    all_cexc_f.write(all_report_do_switches_html)
    pass_cexc_f.close()
    all_cexc_f.close()
    exc_f.close()
    pass_combined_exclusion_do_file = "\"do "+pass_combined_exclusion_do_file+"\""
    all_combined_exclusion_do_file = "\"do "+all_combined_exclusion_do_file+"\""
    pass_vsim_load_cov_cmd = "vsim -cvgperinstance -viewcov "+ pass_ucdb + " -do "+ pass_combined_exclusion_do_file
    all_vsim_load_cov_cmd  = "vsim -cvgperinstance -viewcov "+ all_ucdb  + " -do "+ all_combined_exclusion_do_file
    run_call(pass_vsim_load_cov_cmd,execute_call=False)
    run_call(all_vsim_load_cov_cmd ,execute_call=False)
    print ("=====================")
    print ("Coverage Summary :\n")
    run_call("tail -6 " + pass_cov_merge_file,execute_call=False)
    print ("=====================")

def generate_coverage():
    global pass_ucdb
    global all_ucdb
    global cov_path
    cov_path = regression_path+"/cov"
    pass_ucdb = regression_path+"/cov/pass.ucdb"
    all_ucdb  = regression_path+"/cov/all.ucdb"
    run_call(get_list("mkdir -p "+cov_path))
    run_call(get_list("vcover merge -out "+pass_ucdb)+pass_ucdbs)
    run_call(get_list("vcover merge -out "+all_ucdb )+ucdbs     )
    run_call(get_list("vcover attribute -name TESTNAME "+pass_ucdb+" -stats=+verbose"))
    run_call(get_list("vcover attribute -name TESTNAME "+all_ucdb +" -stats=+verbose"))
    run_call(get_list("vcover report -html "+pass_ucdb+" -output "+cov_path+"/pass_covhtmlreport -details -assert -directive -cvg -code bcefst -threshL 50 -threshH 90"))
    run_call(get_list("vcover report -html "+all_ucdb+"  -output "+cov_path+"/all_covhtmlreport  -details -assert -directive -cvg -code bcefst -threshL 50 -threshH 90"))
    run_call(get_list("vcover report -code sbefc -file "+cov_path+"/pass_coverage.txt "+pass_ucdb))
    report_regression_results(update=False)
    apply_exclution()

# --- Parse Arguments ---
parser = argparse.ArgumentParser()
parser.add_argument("-DUMP",help="DUMP : Default is no ",default='no')
parser.add_argument("-SANITY",help="RUN SANITY TESTS : Default is no ",default='no')
parser.add_argument("-COVERAGE",help="Coverage : Default is yes",default='yes')
parser.add_argument("-TESTLIST",help="Testlist",default='./scripts/testlist.csv')
args = parser.parse_args()
# --- Initialize      ---
PASS_STR = 'TEST_PASSED'
FAIL_STR = 'TEST_FAILED'
FAIL_STR2 = 'UVM_ERROR :    0'
TIMEOUT_STR = 'PH_TIMEOUT'
pass_logs = []
pass_ucdbs = []
fail_logs = []
timeout_logs = []
unknown_logs = []
today = datetime.now()
regression_dir_name="regression_"+today.strftime('%Y%m%d')+ str(today.hour)+str(today.minute)
regression_path = os.getcwd()+"/sim/"+regression_dir_name
regression_report_file = regression_path+'/regression_report.log'
regression_test_list = regression_path+'/testlist.csv'
regression_cmds = regression_path+'/cmds.csh'
cmd = ["mkdir","-p",regression_path]
call(cmd)
tl_f=open(regression_test_list,'w')
print("TESTCASE,SEEDS,SANITY_REGRESS,SEED,CONFIG_DATA,UCI_DATA,NUM_OF_TESTS",file=tl_f)
exclude_file = os.getcwd()+'/scripts/exclusion.do'
manual_exclude_file = os.getcwd()+'/scripts/manual_exclusion.do'
exclude_csv = os.getcwd()+'/scripts/code_coverage_exclusions.csv'
cmds=[]
logs=[]
ucdbs=[]
pass_ucdb = ""
all_ucdb  = ""
cov_path  = ""
test_count = 0
test_count_with_seeds = 0
#--- Generate cmds ---
with open(args.TESTLIST, mode='r') as file:
    test_dict = csv.DictReader(file)
    for testcase in test_dict:
        if("#" in testcase['TESTCASE'] ):
            continue
        if(args.SANITY == 'yes'):
            if(testcase['SANITY_REGRESS']!='yes'):
                continue
            seeds = 1
        else :
            seeds = int(testcase['SEEDS'])
        test_count += 1
        for x in range(seeds):
            plusargs=[]
            if (testcase['SEED']==''):
                seed = random.randrange(100000,999999)
            else:
                seed = int(testcase['SEED'].replace(" ",""))
            if (args.DUMP == 'yes'):
                dump = "DUMP=yes"
            else:
                dump = "DUMP=no"
            if (args.COVERAGE == 'yes'):
                coverage = "COVERAGE=yes"
            else:
                coverage = "COVERAGE=no"
            testdir=regression_path+"/tests/"+testcase['TESTCASE']+"_"+str(seed)
            if(testcase['CONFIG_DATA'].replace(" ","")!=""):
                config_data="PLUS_ARGS+=+CONFIG_DATA="+testcase['CONFIG_DATA']
            else:
                config_data=""
            if(config_data!=""):
                plusargs.append(config_data)
            if(testcase['UCI_DATA'].replace(" ","")!=""):
                uci_data="PLUS_ARGS+=+UCI_DATA="+testcase['UCI_DATA']
            else:
                uci_data=""
            if(uci_data!=""):
                plusargs.append(uci_data)
            if(testcase['NUM_OF_TESTS'].replace(" ","")!=""):
                num_of_tests="PLUS_ARGS+=+NUM_OF_TESTS="+testcase['NUM_OF_TESTS']
            else:
                num_of_tests=""
            if(num_of_tests!=""):
                plusargs.append(num_of_tests)
            cmd = ["make","run",
            "TEST="+testcase['TESTCASE'],
            "SEED="+str(seed),
            "TEST_DIR="+testdir,
            "WORK_DIR="+regression_path+"/work",
            dump,
            coverage
            ]+plusargs
            print(testcase['TESTCASE']+",1,"+testcase['SANITY_REGRESS']+","+str(seed)+","+testcase['CONFIG_DATA']+","+testcase['UCI_DATA']+","+testcase['NUM_OF_TESTS'],file=tl_f)
            logs.append(testdir + "/vsim.log")
            ucdbs.append(testdir + "/"+testcase['TESTCASE']+"_"+str(seed)+".ucdb")
            cmds.append(cmd)
tl_f.close()

run_call(["make","build","WORK_DIR="+regression_path+"/work",coverage])
for cmd in cmds:
    run_call(cmd)
    report_regression_results(update=True)
if (args.COVERAGE == 'yes'):
    generate_coverage()