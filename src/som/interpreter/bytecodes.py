class Bytecodes(object):
    
    # Bytecodes used by the Simple Object Machine (SOM)
    halt             =  0
    dup              =  1
    push_local       =  2
    push_argument    =  3
    push_field       =  4
    push_block       =  5
    push_constant    =  6
    push_global      =  7
    pop              =  8
    pop_local        =  9
    pop_argument     = 10
    pop_field        = 11
    send             = 12
    super_send       = 13
    return_local     = 14
    return_non_local = 15
    
    _num_bytecodes   = 16
    
    _bytecode_length = [ 1, # halt
                         1,  # dup             
                         3,  # push_local      
                         3,  # push_argument   
                         2,  # push_field      
                         2,  # push_block      
                         2,  # push_constant   
                         2,  # push_global     
                         1,  # pop             
                         3,  # pop_local       
                         3,  # pop_argument    
                         2,  # pop_field       
                         2,  # send            
                         2,  # super_send      
                         1,  # return_local    
                         1 ] # return_non_local
    
    _stack_effect_depends_on_message = -1000 # chose a unresonable number to be recognizable
    
    _bytecode_stack_effect = [ 0,                               # halt            
                               1,                               # dup             
                               1,                               # push_local      
                               1,                               # push_argument   
                               1,                               # push_field      
                               1,                               # push_block      
                               1,                               # push_constant   
                               1,                               # push_global     
                              -1,                               # pop             
                              -1,                               # pop_local       
                              -1,                               # pop_argument    
                              -1,                               # pop_field       
                              _stack_effect_depends_on_message, # send            
                              _stack_effect_depends_on_message, # super_send      
                              0,                                # return_local    
                              0 ]                               # return_non_local

    _bytecode_names = ["HALT",
                       "DUP",
                       "PUSH_LOCAL",
                       "PUSH_ARGUMENT",
                       "PUSH_FIELD",
                       "PUSH_BLOCK",
                       "PUSH_CONSTANT",
                       "PUSH_GLOBAL",
                       "POP",
                       "POP_LOCAL",
                       "POP_ARGUMENT",
                       "POP_FIELD",
                       "SEND",
                       "SUPER_SEND",
                       "RETURN_LOCAL",
                       "RETURN_NON_LOCAL"]

def bytecode_length(bytecode):
    return Bytecodes._bytecode_length[bytecode]


def bytecode_stack_effect(bytecode, number_of_arguments_of_message_send = 0):
    if bytecode_stack_effect_depends_on_send(bytecode):
        return -number_of_arguments_of_message_send + 1 # +1 in order to account for the return value
    else:
        return Bytecodes._bytecode_stack_effect[bytecode]


def bytecode_stack_effect_depends_on_send(bytecode):
    assert bytecode >= 0 and bytecode <= Bytecodes._num_bytecodes
    return Bytecodes._bytecode_stack_effect[bytecode] == Bytecodes._stack_effect_depends_on_message


def bytecode_as_str(bytecode):
    if not isinstance(bytecode, int):
        raise ValueError('bytecode is expected to be an integer.')
    assert bytecode >= 0 and bytecode <= Bytecodes._num_bytecodes
    return Bytecodes._bytecode_names[bytecode]
