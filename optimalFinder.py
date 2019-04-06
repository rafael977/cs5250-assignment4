from simulator import RR_scheduling, SJF_scheduling, write_output, read_input

def main():
  process_list = read_input()
  print ("printing input ----")
  for process in process_list:
      print (process)

  min_waiting_time = 999
  min_quantum = 1
  for q in range(1, 11):
    print ("simulating RR with quantum = %d----"%(q))
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = q)
    print('Quantum: %d, average waiting time: %.2f'%(q, RR_avg_waiting_time))
    write_output('RR_%d.txt'%(q), RR_schedule, RR_avg_waiting_time )
    if RR_avg_waiting_time < min_waiting_time:
      min_waiting_time = RR_avg_waiting_time
      min_quantum = q
  print('Min RR waiting time is %.2f when quantum=%d'%(min_waiting_time, min_quantum))

  min_waiting_time = 999
  min_alpha = 0.1
  for i in range(1, 11):
    alpha = i / float(10)
    print ("simulating SJF with alpha = %.2f ----"%alpha)
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = alpha)
    print('Alpha: %.2f, average waiting time: %0.2f'%(alpha, SJF_avg_waiting_time))
    write_output('SJF_%.2f.txt'%alpha, SJF_schedule, SJF_avg_waiting_time )
    if SJF_avg_waiting_time < min_waiting_time:
      min_waiting_time = SJF_avg_waiting_time
      min_alpha = alpha
  print('Min SJF waiting time is %.2f when alpha=%.2f'%(min_waiting_time, min_alpha))

if __name__ == "__main__":
    main()