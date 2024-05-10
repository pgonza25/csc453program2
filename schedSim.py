#!/usr/bin/env python3

import argparse

# Class definition containing all the variables for a Job.
class Job:
    job_number = 0

    arrival_time = 0
    run_time = 0
    cpu_time = 0

    wait_time = 0
    # Turnaround time is the time at which the job completes minus the time at
    # which the job arrived.
    turnaround_time = 0

    completed = False

    def __init__(self, job_number, run_time, arrival_time):
        self.job_number = job_number
        self.run_time = run_time
        self.arrival_time = arrival_time

def fifo(jobs):
    # Process each Job in the order that they are in jobs.
    # First job does not always arrive at time = 0.
    elapsed_time = jobs[0].arrival_time

    for job in jobs:
        if job.arrival_time >= elapsed_time:
            gap = job.arrival_time - elapsed_time
            elapsed_time += gap
        job.wait_time += elapsed_time - job.arrival_time
        elapsed_time += job.run_time
        job.run_time -= job.run_time
        job.turnaround_time += elapsed_time - job.arrival_time

    # Print the data for each job.
    print_job_info(jobs)
    # Compute the average statistics and print them.
    print_average_info(jobs)

def round_robin(jobs, quantum):
    jobs_remaining = len(jobs)
    # First job does not always arrive at time = 0.
    elapsed_time = jobs[0].arrival_time

    # Loop until all jobs have been completed.
    while jobs_remaining > 0:
        for job in jobs:            
            # If there is a gap in jobs, add that time difference.
            if job.arrival_time > elapsed_time:
                gap = elapsed_time - job.arrival_time
                elapsed_time += gap
            # Only work on jobs that have arrived and have not completed.
            if elapsed_time >= job.arrival_time and not job.completed:
                # If a job isn't going to be complete after a quantum.
                if job.run_time > quantum:
                    job.run_time -= quantum
                    elapsed_time += quantum
                    job.cpu_time += quantum
                # If a job is going to be complete after exactly another quantum.
                elif job.run_time == quantum:
                    job.run_time -= quantum
                    elapsed_time += quantum
                    job.cpu_time += quantum
                    job.turnaround_time = elapsed_time - job.arrival_time 
                    job.completed = True
                    job.wait_time = elapsed_time - job.arrival_time - job.cpu_time
                    jobs_remaining -= 1
                # If a job is going to be complete after less than a quantum.
                else:
                    elapsed_time += job.run_time
                    job.cpu_time += job.run_time
                    job.run_time = 0
                    job.turnaround_time = elapsed_time - job.arrival_time
                    job.wait_time = elapsed_time - job.arrival_time - job.cpu_time
                    job.completed = True
                    jobs_remaining -= 1
    # Job is complete, and we can print it's data.
    print_job_info(jobs)
    print_average_info(jobs)

def srtn(jobs):
    elapsed_time = 0
    jobs_remaining = len(jobs)
    # Get the shortest remaining job.
    job = get_shortest_remaining_job(jobs, elapsed_time)
    while jobs_remaining > 0:
        # Work on the job for a unit of time and check again for a new shortest job.
        elapsed_time += 1
        job.run_time -= 1
        job.cpu_time += 1
        # If the job is complete.
        if job.run_time == 0:
            jobs_remaining -= 1
            job.completed = True
            job.wait_time = elapsed_time - job.arrival_time - job.cpu_time
            job.turnaround_time = elapsed_time - job.arrival_time
        job = get_shortest_remaining_job(jobs, elapsed_time)
    # Jobs are complete, print their data.
    print_job_info(jobs)
    print_average_info(jobs)


def get_shortest_remaining_job(jobs, elapsed_time):
    shortest_job = jobs[0]
    for job in jobs:
        if job.run_time < shortest_job.run_time and job.arrival_time <= elapsed_time and job.completed == False:
            shortest_job = job
    return shortest_job
    
def print_job_info(jobs):
    for job in jobs:
        print("Job " + "{:3d}".format(job.job_number) + " -- " + "Turnaround "
            + "{:3.2f}".format(job.turnaround_time) + "  Wait " 
            + "{:3.2f}".format(job.wait_time))

def print_average_info(jobs):
    avg_turnaround = 0
    avg_wait = 0
    for job in jobs:
        avg_turnaround += job.turnaround_time
        avg_wait += job.wait_time
    avg_turnaround /= len(jobs)
    avg_wait /= len(jobs)
    print("Average -- Turnaround {:3.2f}  Wait {:3.2f}".format(avg_turnaround, 
        avg_wait))
    
def main():
    # A list of Job objects.
    jobs = []
    # A list of lists to store run and arrival times of jobs from input file.
    info = []
    # Create an ArgumentParser and add all the possible arguments.
    parser= argparse.ArgumentParser()
    parser.add_argument("filename", help="The name of the file containing jobs",
                        type=str)
    parser.add_argument("-p", nargs=1, help="Scheduling algorithm")
    parser.add_argument("-q", nargs= 1, help="Quantum for Round Robin")

    args = parser.parse_args()

    # Open the file and read the job info from it into input_info.
    try:
        file = open(args.filename, "r")
        line_number = 1
        for line in file:
            data = line.split()
            if len(data) > 0:
                data = [int(data[0]), int(data[1]), line_number]
                info.append(data)
            line_number += 1
    except IOError as e:
        print("File not found.")

    # Sort input_info for tiebreakers.
    info = sorted(info, key=lambda data: (data[1], data[2]))

    # Using input_info, create a list of all the Jobs.
    job_number = 0
    for list in info:
        job = Job(job_number, list[0], list[1])
        jobs.append(job)
        job_number += 1

    # Check for scheduling algorithm. If Round Robin, get quantum.
    if args.p[0] == "SRTN":
        # Run SRTN algorithm and print results.
        srtn(jobs)
        algorithm = args.p[0]
    elif args.p[0] == "RR":
        # Run RR algorithm and print results.
        if args.q is not None:
            round_robin(jobs, int(args.q[0]))
        else:
            round_robin(jobs, 1)
    else:
        # Run FIFO algorithm and print results.
        fifo(jobs)
    
if __name__ == "__main__":
   main()