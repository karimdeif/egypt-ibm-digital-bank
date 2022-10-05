
# Python function for WML deployment:

# Test memory allocation

# See PyFunction_memconfig_Test.ipynb for an example how to use this module.


SampleScoringIput = {'input_data':[   # WML scoring API expects a dictionary with key 'input_data'
            { 'fields': ['low', 'high' ],
              'values':[[1,1.5], [2.9,4], [0,4]]}
    ]  }


import os
    
#wml_python_function
def gen_score_function( ):

    my_status = ["not deployed"]
    
    
    def init_memory() :
        """Run this when the deployment gets created.
        Allocates approx N GB of mem in order to scale the deployment pod.
        The memory is deleted right away. 
        Only want side effect of memory allocation in the pod.
        """
        nonlocal my_status
        
        # large memory allocation to bump up the mem config for the pod
        # Steps are 2GB -> 4GB -> 8GB -> max 16GB
        # E.g. N=9 will result in a pod with 16GB mem 
        # as N is greater than the next lower boundary of 8GB
        N=5
        x = bytearray(1000*1000*1000*N) # N gb
        del x
        
        my_status.append(f"initialized {N} gb mem ")
        print(my_status)

        
        
    init_memory()
    
    my_status.append("deployed")

    
    # The scoring function to be invoked in a WML deployment
    def score(payload) :
        import time
        nonlocal my_status  # shared variable with initialization function
        print("memtest: score started")

        
        # do something that uses lots of memory
        import numpy
        N=6
        score_mem = numpy.random.rand(10000000,13,N)   
        my_status.append(f"allocated {N} GB")
        
        # wait a little so we can check the requested mem for the pod
        time.sleep(20) 
        
    
        # Return scoring result
        score_response = {
            'predictions': [{ 'fields' : 'status', 
                              'values': my_status }]
        } 

        print("memtest: score return")
        return score_response
        
    # in outer function
    return score    # return function
