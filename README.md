# CSC 453: Program 2
# Scheduler Simulator

Name: Pablo Gonzalez

Term: Spring 2024

1. SRTN delivers the same turnaround times as FIFO for workloads where shorter jobs
arrive before longer ones or where all jobs are equal length.

2. SRTN delivers the same response times as RR when jobs arrive in ascending order
and when the RR quantum is longer than all of the jobs and therefore no jobs exhaust
their quantum before completing.

3. Response time increases as job length increases with SRTN. To see this trend
with the simulator, simply hand it a list of jobs that increase in length. A job can 
be the shortest remaining and still be long, and longer jobs can get stuck behind a
handful of shorter, but still lengthy, jobs.

4. Assuming that job lengths are not less than the quantum length, response time
increases as quantum length increases. This is because jobs that are not currently scheduled
have to wait the quantum length * the number of other jobs still processing for another
turn on the CPU.