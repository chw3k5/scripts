def param_array(zero_array, first_array, zero_len, first_len):
    import numpy
    loop_over = (first_len) - 1
    temp0_array = zero_array
    new_len = zero_len*first_len
    for n in range(loop_over):
        temp0_array = numpy.vstack((temp0_array, zero_array))
    zero_array = temp0_array
    zero_array = numpy.reshape(zero_array, new_len)
    
    loop_over = (zero_len) - 1
    temp1_array = first_array
    for n in range(loop_over):
        temp1_array = numpy.vstack((temp1_array, first_array))
    first_array = numpy.transpose(temp1_array)
    first_array = numpy.reshape(first_array, new_len)
    zero_len    = new_len
    first_len   = new_len
    return zero_array, first_array, zero_len, first_len