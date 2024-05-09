#!/usr/bin/env python3

import argparse

# A list of Job objects. 
jobs = []
# Class definition containing all the variables for a Job.
class Job:
    job_number = 0

    arrival_time = 0
    burst_time = 0
    run_time = 0

    wait_time = 0
    turnaround_time = 0

    def __init__(self, job_number, arrival_time, run_time):
        self.job_number = job_number
        self.arrival_time = arrival_time
        self.run_time = run_time
    
    

def main():
    # A list of lists to store run and arrival times of jobs from input file.
    input_info = []
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
        for line in file:
            data = [int(x) for x in line.split()]
            print(data)
            print(data[0])
    except IOError as e:
        print("File not found.")

if __name__ == "__main__":
   main()
