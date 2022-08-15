import time
import smbus

bus = smbus.SMBus(1)
ADDRESS = 0x20


def read_16_bit_val(addr):
    val = bus.read_byte_data(ADDRESS,addr)
    val *= 256
    val += bus.read_byte_data(ADDRESS, addr+1)
    return val

def write_16_bit_val(addr, val):
    (olderbyte, youngerbyte) = val.to_bytes(2, byteorder="big")
    bus.write_byte_data(ADDRESS,addr, olderbyte)
    bus.write_byte_data(ADDRESS, addr + 1, youngerbyte)    


def set_current(val):
    ''' sets "set" current for internal regulator '''
    if (val < 0.0 or val > 2.0):
        print("bad current value")
        return
    raw_val =int( (val / 3.3) * 4096)
    write_16_bit_val( 1, raw_val)
    bus.write_byte_data( ADDRESS, 3, 0x01) # confirm funushing sending data.


def get_set_current():
    val = int(read_16_bit_val(1))
    return (val /4096) *3.3

def get_output_val():
    ''' gets output pwm val '''
    return bus.read_byte_data(ADDRESS, 0)


def get_input_val():
    ''' this method gets reading from analog voltage sensor '''
    val = read_16_bit_val(4)
    return (val / 4096) * 3.3

def enable_regulator():
    ''' sets val whutch enables internal regulator '''
    bus.write_byte_data(ADDRESS, 6, 0x01)

def disable_regulator():
    ''' sets val whitch disables internal regulator '''
    bus.write_byte_data(ADDRESS, 6, 0x00)

def get_mode():
    '''gets current setting'''
    return bus.read_byte_data(ADDRESS, 6)

def print_status():
    ''' prints all cc board values '''
    output_val = get_output_val()
    real_current = get_input_val()
    set_current = get_set_current()
    mode = get_mode()
    print("Board no:", ADDRESS, " mode: ", mode )
    print("PWM val: ", output_val)
    print("Set curr:", set_current, "Real curr", real_current)



if __name__ == '__main__':
    print("ConstantCurrent Interface INIT")
    pwmPercent = bus.read_byte_data(ADDRESS, 0)
    disable_regulator()   
    enable_regulator()
    set_current(0.3)
    
    print_status()
