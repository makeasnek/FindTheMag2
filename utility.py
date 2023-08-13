# Used for debugging purposes
import main
def generate_stats():
    answer=input('Enter BOINC data dir')
    combined_stats = main.config_files_to_stats(answer)
    example_ratios = {
        'WORLDCOMMUNITYGRID.ORG': .01,
        'SECH.ME/BOINC/AMICABLE': .99,
        'ESCATTER11.FULLERTON.EDU/NFS': .0,
    }
    approved_projects = list(example_ratios.keys())
    result=main.add_mag_to_combined_stats(combined_stats, example_ratios, approved_projects, preferred_projects=[])
    print('Answer is {}'.format(result))
if __name__=='__main__':
    answer=''
    while True:
        print('1. Generate stats')
        answer=input('Enter the option you would like to choose, or Q for quit')
        if answer=='1':
            generate_stats()
        if answer=='Q':
            quit()
