'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
from operator import attrgetter

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

class ExtendedProcess(Process):
    def __init__(self, id, arrive_time, burst_time):
        super().__init__(id, arrive_time, burst_time)
        self.completion_time = arrive_time + burst_time
        self.remaining_time = burst_time

    def getWaitingTime(self):
        return self.completion_time - self.arrive_time - self.burst_time

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    ext_process_list = [ExtendedProcess(p.id, p.arrive_time, p.burst_time) for p in process_list]
    schedule = []
    current_time = 0
    completed_count = 0
    total_count = len(ext_process_list)

    while completed_count < total_count:
        # print(completed_count, total_count)
        is_idle = True
        for process in ext_process_list:
            if process.arrive_time <= current_time and process.remaining_time > 0:
                # print("processing ", process.id, current_time)
                schedule.append((current_time, process.id))
                is_idle = False
                if time_quantum < process.remaining_time:
                    current_time += time_quantum
                    process.remaining_time -= time_quantum
                else:
                    # print(process.id, "completed")
                    current_time += process.remaining_time
                    process.remaining_time = 0
                    process.completion_time = current_time
                    completed_count += 1
        if is_idle:
            g = (process for process in ext_process_list if process.remaining_time > 0)
            current_time = next(g).arrive_time

    average_waiting_time = sum([process.getWaitingTime() for process in ext_process_list])/float(total_count)
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    ext_process_list = [ExtendedProcess(p.id, p.arrive_time, p.burst_time) for p in process_list]
    schedule = []
    current_time = 0
    completed_count = 0
    total_count = len(ext_process_list)
    min_id = -1

    while completed_count < total_count:
        processs_shortlist = [process for process in ext_process_list if process.arrive_time <= current_time and process.remaining_time > 0]
        if len(processs_shortlist) > 0:
            process_shortest = min(processs_shortlist, key=attrgetter("remaining_time"))
            if min_id != process_shortest.id:
                min_id = process_shortest.id
                schedule.append((current_time, process_shortest.id))

            current_time += 1
            process_shortest.remaining_time -= 1

            if process_shortest.remaining_time == 0:
                process_shortest.completion_time = current_time
                completed_count += 1
        else:
            g = (process for process in ext_process_list if process.remaining_time > 0)
            current_time = next(g).arrive_time

    average_waiting_time = sum([process.getWaitingTime() for process in ext_process_list])/float(total_count)
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    ext_process_list = [ExtendedProcess(p.id, p.arrive_time, p.burst_time) for p in process_list]
    schedule = []
    current_time = 0
    completed_count = 0
    total_count = len(ext_process_list)
    process_history = {}

    while completed_count < total_count:
        processs_shortlist = [process for process in ext_process_list if process.arrive_time <= current_time and process.remaining_time > 0]
        if len(processs_shortlist) > 0:
            min_guess_time = 999
            min_process = None
            for process in processs_shortlist:
                if process_history.get(process.id) == None:
                    guess = 5
                else:
                    last_burst, last_guess = process_history.get(process.id)
                    guess = alpha * last_burst + (1 - alpha) * last_guess
                if guess < min_guess_time:
                    min_guess_time = guess
                    min_process = process

            process_history[min_process.id] = (min_process.burst_time, min_guess_time)
            schedule.append((current_time, min_process.id))
            current_time += min_process.burst_time
            min_process.completion_time = current_time
            min_process.remaining_time = 0
            completed_count += 1
        else:
            g = (process for process in ext_process_list if process.remaining_time > 0)
            current_time = next(g).arrive_time

    average_waiting_time = sum([process.getWaitingTime() for process in ext_process_list])/float(total_count)
    return schedule, average_waiting_time


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)

    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

